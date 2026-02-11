# vLLM 0.11.2 → 0.14.1 Migration Plan

## Overview

Upgrading HuggingFace server from vLLM 0.11.2 to 0.14.1 to address bug fixes and security improvements.

**References:**
- [vLLM v0.14.1 Release](https://github.com/vllm-project/vllm/releases/tag/v0.14.1)
- [vLLM v0.14.0 Release](https://github.com/vllm-project/vllm/releases/tag/v0.14.0)
- [KServe PR #4990](https://github.com/kserve/kserve/pull/4990) (vLLM 0.14.0 upgrade)

## Breaking Changes from 0.11.2 to 0.14.1

### 1. PyTorch Version Requirement
- **Change**: PyTorch 2.9.1+ is now required
- **Impact**: May require base image updates
- **Action**: Verify PyTorch version in Dockerfiles

### 2. Async Scheduling (Default Enabled)
- **Change**: Async scheduling is now enabled by default
- **Impact**: Performance improvements but may change behavior
- **Option**: Can disable with `--no-async-scheduling` if issues arise
- **Exceptions**: Disabled automatically for:
  - Pipeline parallel
  - CPU backend
  - Non-MTP/Eagle spec decoding

### 3. Deprecated Quantization Schemes Removed
- **Impact**: Any deprecated quantization configs will fail
- **Action**: Review and update quantization parameters

### 4. Speculative Decoding Parameters
- **Change**: Unsupported sampling parameters now fail explicitly
- **Impact**: Better error reporting, may catch previously silent issues

### 5. CUDA Version
- **Change**: Default wheel compiled against cu129
- **Impact**: May need to specify correct CUDA version

## New Features in 0.14.0/0.14.1

### Major Features
- **gRPC Server Entrypoint**: Binary protocol with HTTP/2 multiplexing
- **Automatic Context Length**: `--max-model-len auto` fits to GPU memory
- **Model Inspection**: View module structure, attention backends, quantization
- **Model Runner V2**: Enhanced with UVA block tables, M-RoPE (experimental)

### API Additions
- `/server_info` endpoint for environment information
- `attention_config` parameter in LLM()
- Enhanced `/embeddings` endpoint with `continue_final_message`
- `reasoning_effort` parameter support

### Model Support
- 8 new architectures (Grok-2, LFM2-VL, openPangu MoE, etc.)
- Extensive LoRA expansion for multimodal models

## Files to Update

Based on PR #4990 and our codebase:

### 1. `python/kserve/pyproject.toml`
- Update: `vllm==0.14.1` (currently 0.11.2)
- Verify: PyTorch version compatibility

### 2. `python/huggingfaceserver/huggingfaceserver/vllm/utils.py`
- Check: `AsyncEngineArgs` API changes
- Verify: `build_vllm_engine_args()` compatibility
- Test: Remote URI detection still works

### 3. `python/huggingfaceserver/huggingfaceserver/vllm/vllm_model.py`
- Check: `build_async_engine_client_from_engine_args()` changes
- Verify: `AsyncLLM.from_vllm_config()` signature
- Update: Any deprecated parameters

### 4. `python/kserve/kserve/protocol/rest/openai/types/__init__.py`
- Update: OpenAI protocol types if changed in 0.14
- Check: New parameters or fields

### 5. `python/huggingfaceserver/uv.lock`
- Run: `make uv-lock` to update all dependencies
- Resolve: Any version conflicts

### 6. `python/huggingfaceserver/pyproject.toml`
- Verify: No local overrides needed

## Implementation Plan

### Phase 1: Dependency Updates
1. Update vLLM version in `python/kserve/pyproject.toml`
2. Run `make uv-lock` to update lock files
3. Check for dependency conflicts

### Phase 2: Code Updates
1. Review `vllm/utils.py` for API changes
2. Update `vllm/vllm_model.py` if needed
3. Update OpenAI types if changed
4. Ensure our S3/RunAI streamer changes are compatible

### Phase 3: Testing
1. Test with standard HuggingFace model IDs
2. Test with S3 URIs + RunAI streamer
3. Test async scheduling behavior
4. Test with different model types (generative, encoder)

### Phase 4: Documentation
1. Update README with any new requirements
2. Document new features available in 0.14.1
3. Note breaking changes for users

## Known Issues from PR #4990

The PR author noted they "can't pass the test" - specifically:
- `TestServerTimeout` failed with segmentation violation
- Router component issue

**Investigation needed:**
- Check if issue is resolved in 0.14.1
- Review test failures and determine if they affect us

## Migration Checklist

- [ ] Update `python/kserve/pyproject.toml`: vllm==0.14.1
- [ ] Review `vllm/utils.py` for AsyncEngineArgs changes
- [ ] Review `vllm/vllm_model.py` for engine initialization changes
- [ ] Check OpenAI protocol types updates
- [ ] Run `make uv-lock` in kserve and huggingfaceserver
- [ ] Verify PyTorch version compatibility
- [ ] Test with standard HuggingFace models
- [ ] Test with S3 URIs + RunAI streamer
- [ ] Test async scheduling (enabled by default)
- [ ] Run existing test suite
- [ ] Update documentation
- [ ] Create migration notes for users

## Potential Risks

1. **Async Scheduling Changes**: May affect request processing order/behavior
2. **PyTorch Version**: Older images may not have PyTorch 2.9.1
3. **CUDA Compatibility**: cu129 default may require CUDA updates
4. **Breaking API Changes**: Need to verify all AsyncEngineArgs parameters
5. **Test Failures**: PR #4990 had test issues we should investigate

## Rollback Plan

If issues arise:
1. Revert vLLM version to 0.11.2
2. Revert uv.lock files
3. Document issues found
4. Option: Try intermediate version (0.13.x) as stepping stone

## Next Steps

1. Review actual code changes from PR #4990 in detail
2. Check vLLM 0.14.1 source code for AsyncEngineArgs API
3. Test locally with small model
4. Create comprehensive test plan
5. Document any additional changes needed

## Resources

- [vLLM Engine Arguments Docs](https://docs.vllm.ai/en/stable/configuration/engine_args/)
- [AsyncLLMEngine API](https://docs.vllm.ai/en/latest/dev/engine/async_llm_engine.html)
- [vLLM Releases](https://github.com/vllm-project/vllm/releases)
- [KServe PR #4990](https://github.com/kserve/kserve/pull/4990)
