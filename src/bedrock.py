# 参考 : https://qiita.com/moritalous/items/5c12ca179fac7ca416c3
import random
import boto3
import json
from config import AWS_CONFIG

client = boto3.client(
    "bedrock-agent-runtime",
    region_name=AWS_CONFIG['REGION_NAME'],
    aws_access_key_id=AWS_CONFIG['ACCESS_KEY_ID'],
    aws_secret_access_key=AWS_CONFIG['SECRET_ACCESS_KEY']
)

class BaseAgent:
    """Bedrockエージェントの基本クラス"""

    def __init__(self, foundation_model="anthropic.claude-3-sonnet-20240229-v1:0"):
        """
        BaseAgentのコンストラクタ

        Args:
            foundation_model: 使用する基盤モデル名
        """
        self.foundation_model = foundation_model
        self.action_groups = []
        self.instruction = ""
        self.client = client

    def invoke(self, input_text, session_id=None, enable_trace=False):
        """
        エージェントを呼び出して実行する

        Args:
            input_text: ユーザー入力テキスト
            session_id: セッションID（Noneの場合は自動生成）
            enable_trace: トレースを有効にするかどうか

        Returns:
            エージェント実行結果
        """
        # セッションIDがない場合は自動生成
        if session_id is None:
            random_int = random.randint(1, 100000)
            session_id = f"session-id-{random_int}"

        return self._invoke_agent(
            session_id=session_id,
            input_text=input_text,
            enableTrace=enable_trace
        )

    def _invoke_agent(self, session_id, input_text, enableTrace=False):
        """
        Bedrockエージェントを呼び出して実行する（内部メソッド）

        Args:
            session_id: セッションID
            input_text: ユーザー入力テキスト
            enableTrace: トレースを有効にするかどうか

        Returns:
            エージェント実行結果
        """
        def generate_function_schema(func):
            import inspect

            sig = inspect.signature(func)

            parameters = {}
            for param_name, param in sig.parameters.items():
                # 型アノテーションを取得
                param_type = (
                    param.annotation.__name__
                    if param.annotation != inspect.Parameter.empty
                    else "any"
                )

                # Pythonの型をJSONスキーマの型に変換
                type_mapping = {
                    "int": "integer",
                    "str": "string",
                    "float": "number",
                    "bool": "boolean",
                    "list": "array",
                    "dict": "object",
                }
                json_type = type_mapping.get(param_type, param_type)

                parameters[param_name] = {"type": json_type, "required": True}

            # スキーマを構築
            schema = {
                "actionGroupName": func.__name__,
                "functionSchema": {
                    "functions": [
                        {
                            "name": func.__name__,
                            "description": func.__doc__,
                            "parameters": parameters,
                        }
                    ]
                },
                "actionGroupExecutor": {"customControl": "RETURN_CONTROL"},
            }

            return schema

        response = self.client.invoke_inline_agent(
            sessionId=session_id,
            foundationModel=self.foundation_model,
            actionGroups=[generate_function_schema(action) for action in self.action_groups],
            instruction=self.instruction,
            inputText=input_text,
            enableTrace=enableTrace,
        )

        chunk = []
        return_control = []

        for event in response["completion"]:
            if "chunk" in event:
                chunk.append(event["chunk"])
            if "returnControl" in event:
                return_control.append(event["returnControl"])
            if "trace" in event:
                print(event["trace"])

        while len(return_control):
            session_state = None

            for r in return_control:
                invocation_id = r["invocationId"]
                invocation_inputs = r["invocationInputs"]

                session_state = {
                    "invocationId": invocation_id,
                    "returnControlInvocationResults": [],
                }

                for inputs in invocation_inputs:
                    invocation_input = inputs["functionInvocationInput"]

                    action_group = invocation_input["actionGroup"]
                    function = invocation_input["function"]
                    parameters = invocation_input["parameters"]

                    # アクションにわたすパラメーター
                    input = {
                        parameter["name"]: parameter["value"] for parameter in parameters
                    }
                    # アクションの名前と関数のディクショナリーを生成
                    action_groups_dict = {
                        action.__name__: action for action in self.action_groups
                    }
                    # ディクショナリーからアクションを取得して実行
                    action_result = action_groups_dict[function](**input)

                    session_state["returnControlInvocationResults"].append(
                        {
                            "functionResult": {
                                "actionGroup": action_group,
                                "function": function,
                                "responseBody": {
                                    "TEXT": {
                                        "body": json.dumps(
                                            action_result, ensure_ascii=False
                                        )
                                    }
                                },
                            }
                        }
                    )

            response = self.client.invoke_inline_agent(
                sessionId=session_id,
                foundationModel=self.foundation_model,
                actionGroups=[generate_function_schema(action) for action in self.action_groups],
                instruction=self.instruction,
                enableTrace=enableTrace,
                inlineSessionState=session_state,  # セッション情報
            )

            return_control = []

            for event in response["completion"]:
                if "chunk" in event:
                    chunk.append(event["chunk"])
                if "returnControl" in event:
                    return_control.append(event["returnControl"])
                if "trace" in event:
                    print(event["trace"])

        return chunk[0]["bytes"].decode()

class SampleAgent(BaseAgent):
    """サンプルエージェント"""

    def __init__(self, foundation_model="anthropic.claude-3-sonnet-20240229-v1:0"):
        """
        SampleAgentのコンストラクタ

        Args:
            foundation_model: 使用する基盤モデル名
        """
        super().__init__(foundation_model)
        self.instruction = """
        あなたは日常会話をするエージェントです。
        ユーザーからの入力に対して、適切な回答をしてください。
        """
