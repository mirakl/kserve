#!/usr/bin/env python3
"""
Quick test script to validate vLLM 0.15.1 API compatibility.
Tests ALL vLLM imports used across the huggingfaceserver codebase.

Run this locally to catch API issues before building Docker images.

Usage:
    python test_vllm_migration.py
"""

import sys
from typing import List, Tuple

def test_imports() -> List[Tuple[str, bool, str]]:
    """Test all critical imports from vLLM 0.14.1"""
    results = []

    # Test 1: AsyncEngineArgs import
    try:
        from vllm.engine.arg_utils import AsyncEngineArgs
        results.append(("AsyncEngineArgs import", True, ""))
    except Exception as e:
        results.append(("AsyncEngineArgs import", False, str(e)))

    # Test 2: Embedding protocol imports
    try:
        from vllm.entrypoints.pooling.embed.protocol import (
            EmbeddingRequest,
            EmbeddingResponse,
            EmbeddingResponseData,
            EmbeddingCompletionRequest
        )
        results.append(("Embedding protocol imports", True, ""))
    except Exception as e:
        results.append(("Embedding protocol imports", False, str(e)))

    # Test 3: Rerank protocol imports
    try:
        from vllm.entrypoints.pooling.score.protocol import (
            RerankRequest,
            RerankResponse
        )
        results.append(("Rerank protocol imports", True, ""))
    except Exception as e:
        results.append(("Rerank protocol imports", False, str(e)))

    # Test 4: Serving class imports (pooling)
    try:
        from vllm.entrypoints.pooling.embed.serving import OpenAIServingEmbedding
        from vllm.entrypoints.pooling.score.serving import ServingScores
        results.append(("Pooling serving class imports", True, ""))
    except Exception as e:
        results.append(("Pooling serving class imports", False, str(e)))

    # Test 4b: Serving class imports (OpenAI - vLLM 0.15+ reorganized)
    try:
        from vllm.entrypoints.openai.completion.serving import OpenAIServingCompletion
        from vllm.entrypoints.openai.chat_completion.serving import OpenAIServingChat
        results.append(("OpenAI serving class imports", True, ""))
    except Exception as e:
        results.append(("OpenAI serving class imports", False, str(e)))

    # Test 5: ToolParserManager import
    try:
        from vllm.tool_parsers import ToolParserManager
        results.append(("ToolParserManager import", True, ""))
    except Exception as e:
        results.append(("ToolParserManager import", False, str(e)))

    # Test 6: OpenAI protocol imports (vLLM 0.15+ reorganized into subdirectories)
    try:
        from vllm.entrypoints.openai.chat_completion.protocol import (
            ChatCompletionRequest,
            ChatCompletionResponse
        )
        from vllm.entrypoints.openai.completion.protocol import (
            CompletionRequest,
            CompletionResponse
        )
        results.append(("OpenAI protocol imports", True, ""))
    except Exception as e:
        results.append(("OpenAI protocol imports", False, str(e)))

    # Test 7: Engine and utility imports
    try:
        from vllm.engine.protocol import EngineClient
        from vllm.entrypoints.logger import RequestLogger
        results.append(("Engine and logger imports", True, ""))
    except Exception as e:
        results.append(("Engine and logger imports", False, str(e)))

    # Test 8: CLI args and models (vLLM 0.15+ reorganized)
    try:
        from vllm.entrypoints.openai.cli_args import make_arg_parser, validate_parsed_serve_args
        from vllm.entrypoints.openai.models.protocol import BaseModelPath
        from vllm.entrypoints.openai.models.serving import OpenAIServingModels
        results.append(("CLI args and models imports", True, ""))
    except Exception as e:
        results.append(("CLI args and models imports", False, str(e)))

    # Test 9: Chat utils (vLLM 0.15+ load_chat_template replaced process_chat_template)
    try:
        from vllm.entrypoints.chat_utils import load_chat_template
        results.append(("Chat utils (load_chat_template)", True, ""))
    except Exception as e:
        results.append(("Chat utils (load_chat_template)", False, str(e)))

    # Test 10: Model loader and tokenizer
    try:
        from vllm.model_executor.model_loader import get_model_loader
        from vllm.transformers_utils.tokenizer import get_tokenizer
        results.append(("Model loader and tokenizer imports", True, ""))
    except Exception as e:
        results.append(("Model loader and tokenizer imports", False, str(e)))

    # Test 11: Reasoning parser
    try:
        from vllm.reasoning import ReasoningParserManager
        results.append(("ReasoningParserManager import", True, ""))
    except Exception as e:
        results.append(("ReasoningParserManager import", False, str(e)))

    # Test 12: Argument parser utils
    try:
        from vllm.utils.argparse_utils import FlexibleArgumentParser
        results.append(("FlexibleArgumentParser import", True, ""))
    except Exception as e:
        results.append(("FlexibleArgumentParser import", False, str(e)))

    # Test 13: Engine protocol ErrorResponse
    try:
        from vllm.entrypoints.openai.engine.protocol import ErrorResponse
        results.append(("ErrorResponse import (engine.protocol)", True, ""))
    except Exception as e:
        results.append(("ErrorResponse import (engine.protocol)", False, str(e)))

    return results


def test_api_attributes() -> List[Tuple[str, bool, str]]:
    """Test AsyncEngineArgs attributes"""
    results = []

    try:
        from vllm.engine.arg_utils import AsyncEngineArgs

        # Test 7: Check enable_log_requests exists
        engine_args = AsyncEngineArgs(model="dummy")
        if hasattr(engine_args, 'enable_log_requests'):
            results.append(("AsyncEngineArgs.enable_log_requests", True, ""))
        else:
            results.append(("AsyncEngineArgs.enable_log_requests", False, "Attribute not found"))

        # Test 8: Check disable_log_stats exists
        if hasattr(engine_args, 'disable_log_stats'):
            results.append(("AsyncEngineArgs.disable_log_stats", True, ""))
        else:
            results.append(("AsyncEngineArgs.disable_log_stats", False, "Attribute not found"))

        # Test 9: Verify enable_log_stats does NOT exist
        if not hasattr(engine_args, 'enable_log_stats'):
            results.append(("Verify enable_log_stats doesn't exist", True, "Correctly absent"))
        else:
            results.append(("Verify enable_log_stats doesn't exist", False, "Attribute exists (shouldn't!)"))

    except Exception as e:
        results.append(("AsyncEngineArgs attributes", False, str(e)))

    return results


def test_asyncllm_signature() -> List[Tuple[str, bool, str]]:
    """Test AsyncLLM.from_vllm_config signature"""
    results = []

    try:
        from vllm.v1.engine.async_llm import AsyncLLM
        import inspect

        # Get the signature of from_vllm_config
        sig = inspect.signature(AsyncLLM.from_vllm_config)
        params = list(sig.parameters.keys())

        # Test 10: Check for enable_log_requests parameter
        if 'enable_log_requests' in params:
            results.append(("AsyncLLM.from_vllm_config has enable_log_requests", True, ""))
        else:
            results.append(("AsyncLLM.from_vllm_config has enable_log_requests", False, "Parameter not found"))

        # Test 11: Check for disable_log_stats parameter
        if 'disable_log_stats' in params:
            results.append(("AsyncLLM.from_vllm_config has disable_log_stats", True, ""))
        else:
            results.append(("AsyncLLM.from_vllm_config has disable_log_stats", False, "Parameter not found"))

    except Exception as e:
        results.append(("AsyncLLM.from_vllm_config signature", False, str(e)))

    return results


def print_results(results: List[Tuple[str, bool, str]]):
    """Print test results in a nice format"""
    print("\n" + "="*80)
    print("vLLM 0.15.1 Migration Test Results")
    print("="*80 + "\n")

    passed = 0
    failed = 0

    for test_name, success, error in results:
        if success:
            print(f"✅ PASS: {test_name}")
            if error:
                print(f"         {error}")
            passed += 1
        else:
            print(f"❌ FAIL: {test_name}")
            print(f"         Error: {error}")
            failed += 1

    print("\n" + "="*80)
    print(f"Summary: {passed} passed, {failed} failed")
    print("="*80 + "\n")

    return failed == 0


def main():
    """Run all tests"""
    print("\nTesting vLLM 0.15.1 API compatibility...")
    print("This will validate that all imports and API changes are correct.\n")

    all_results = []

    print("Running import tests...")
    all_results.extend(test_imports())

    print("Testing API attributes...")
    all_results.extend(test_api_attributes())

    print("Testing method signatures...")
    all_results.extend(test_asyncllm_signature())

    # Print results
    success = print_results(all_results)

    if success:
        print("🎉 All tests passed! The vLLM 0.15.1 migration looks good.")
        print("You can proceed with building the Docker image.")
        return 0
    else:
        print("⚠️  Some tests failed. Fix the issues before building Docker image.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
