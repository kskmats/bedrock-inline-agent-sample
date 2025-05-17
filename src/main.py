#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from bedrock import SampleAgent
def main():
    sample_agent = SampleAgent()
    print(sample_agent.invoke("こんにちは"))


if __name__ == "__main__":
    main()