#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from bedrock import SampleAgent
def main():
    sample_agent = SampleAgent()
    print(sample_agent.invoke("本日の日付を教えてください！"))


if __name__ == "__main__":
    main()