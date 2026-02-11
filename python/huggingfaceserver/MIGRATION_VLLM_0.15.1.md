# vLLM 0.14.1 → 0.15.1 Migration Summary

## Overview

Upgrading HuggingFace server from vLLM 0.14.1 to 0.15.1 for performance improvements, bug fixes, and security updates.

**Migration Difficulty:** LOW ✅
**Code Changes Required:** NONE ✅
**Dependency Updates Only:** YES ✅

**References:**
- [vLLM v0.15.1 Release](https://github.com/vllm-project/vllm/releases/tag/v0.15.1)
- [vLLM v0.15.0 Release](https://github.com/vllm-project/vllm/releases/tag/v0.15.0)

## Summary of Changes

### ✅ What Changed
- **vLLM:** 0.14.1 → 0.15.1
- **FlashInfer:** 0.5.3 → 0.6.1 (3-4x faster torch.compile cold-start)
- **aiohttp:** 3.11.16 → 3.13.3 (Security: CVE-2025-69223)
- **apache-tvm-ffi:** 0.1.3 → 0.1.8.post2
- **nvidia-cutlass-dsl:** 4.3.0 → 4.3.5

### ✅ What DIDN'T Change (Good News!)
- **All import paths** - No changes needed
- **All API signatures** - AsyncEngineArgs, AsyncLLM.from_vllm_config() unchanged
- **All parameters** - enable_log_requests, disable_log_stats stay the same
- **All serving classes** - OpenAIServingEmbedding, ServingScores unchanged
- **S3/RunAI streamer** - Still works

## Files Modified

### 1. `/Users/yannick.lambruschi/repos/kserve/python/kserve/pyproject.toml`
```diff
llm = [
-   "vllm==0.14.1",
+   "vllm==0.15.1",
]
```

### 2. `/Users/yannick.lambruschi/repos/kserve/python/huggingface_server.Dockerfile`
```diff
-ARG VLLM_VERSION=0.14.1
+ARG VLLM_VERSION=0.15.1
-ARG FLASHINFER_VERSION=0.5.3
+ARG FLASHINFER_VERSION=0.6.1
```

### 3. `/Users/yannick.lambruschi/repos/kserve/python/huggingface_server_cpu.Dockerfile`
```diff
-ARG VLLM_VERSION=0.14.1
+ARG VLLM_VERSION=0.15.1
```

### 4. `/Users/yannick.lambruschi/repos/kserve/python/huggingfaceserver/tests/setup_vllm.sh`
```diff
-VLLM_VERSION=v0.14.1
+VLLM_VERSION=v0.15.1
```

### 5. Lock Files
- `python/kserve/uv.lock` - Updated via `uv lock`
- `python/huggingfaceserver/uv.lock` - Updated via `uv lock`

## Breaking Changes

### None That Affect Our Code ✅

The following breaking changes exist in 0.15.x but **do not affect our implementation**:

1. **PoolingParams API changes** - Internal to serving classes (we don't use directly)
2. **Metrics renamed** - `vllm:time_per_output_token_seconds` → `vllm:inter_token_latency_seconds` (monitoring only)
3. **Quantization methods removed** - DeepSpeedFp8, RTN (we don't use these)

## Benefits

### Performance Improvements
- **torch.compile cold-start:** 88s → 22s (for Llama3-70B) - 4x faster!
- **FlashInfer 0.6.1:** Better MoE kernel performance on RTX Blackwell GPUs
- **V1 engine optimizations:** Better CPU/GPU overlap (already using since 0.14)

### Bug Fixes
- **Prefix cache hit rates:** Fixed in 0.15.1
- **Speculative decoding metrics:** Fixed in 0.15.1
- **ROCm GEMM dispatch:** Fixed in 0.15.1

### Security Fixes
- **CVE-2025-69223:** aiohttp vulnerability patched
- **CVE-2026-0994:** Protobuf vulnerability patched (already fixed in 0.14.1)

### New Features Available
- **API Enhancements:**
  - `prompt_cache_key` in responses
  - `include_stop_str_in_output` tuning
  - `skip_special_tokens` configuration
- **Model Support:**
  - 8 new architectures supported
  - LoRA expansion for multimodal models

## Testing Checklist

### Pre-Deployment Testing

- [ ] **Import test:** Run `python test_vllm_migration.py`
- [ ] **Basic chat:** Test chat completions endpoint
- [ ] **Embeddings:** Test embeddings endpoint
- [ ] **Reranking:** Test reranking endpoint
- [ ] **S3 + RunAI:** Test model loading from S3 with RunAI streamer
- [ ] **LoRA:** Test LoRA adapter loading (if used)
- [ ] **Tool Calling:** Test tool calling (if used)

### Performance Testing

- [ ] **Throughput:** Measure requests/second vs 0.14.1
- [ ] **Latency:** Measure time-to-first-token and inter-token latency
- [ ] **Memory:** Monitor GPU memory usage
- [ ] **Expected:** Equal or better performance (FlashInfer 0.6.1 improvements)

### Integration Testing

- [ ] **Health checks:** `/healthz`, `/v1/models`
- [ ] **All endpoints:** `/v1/chat/completions`, `/v1/completions`, `/v1/embeddings`, `/v1/rerank`
- [ ] **Metrics:** Verify Prometheus metrics endpoint
- [ ] **Logs:** Check for warnings or errors

### Stress Testing

- [ ] **Concurrent requests:** 10+ concurrent users
- [ ] **Long-running:** 1+ hour continuous operation
- [ ] **Memory leaks:** Monitor for degradation

## Rollback Plan

If issues arise, rollback is straightforward since only dependency versions changed:

```bash
# Revert to 0.14.1
git revert HEAD
# Or manually change versions back:
# - pyproject.toml: vllm==0.14.1
# - Dockerfiles: VLLM_VERSION=0.14.1, FLASHINFER_VERSION=0.5.3
# - test script: VLLM_VERSION=v0.14.1
# Then run: uv lock in both python/kserve and python/huggingfaceserver
```

## Known Issues

### Low Risk
- **PyTorch 2.10 on macOS:** vLLM 0.15.x has import issues on Darwin (not applicable to Linux GPU deployments)
- **PoolingParams deprecation:** Internal to serving classes, should be transparent

## Compatibility

- ✅ **Python:** 3.10, 3.11, 3.12 (unchanged)
- ✅ **PyTorch:** 2.9.1+ (unchanged)
- ✅ **CUDA:** 12.9+ (unchanged)
- ✅ **Protobuf:** 6.30.0+ (unchanged from 0.14.1)
- ✅ **KServe:** All versions (no KServe API changes)

## Migration Timeline

**Estimated Time:** 1-2 weeks for full deployment

- **Week 1:** Update dependencies, local testing, Docker build, test environment deployment
- **Week 2:** Performance testing, monitoring, production deployment

## References

### Release Notes
- [vLLM v0.15.1 Release](https://github.com/vllm-project/vllm/releases/tag/v0.15.1)
- [vLLM v0.15.0 Release](https://github.com/vllm-project/vllm/releases/tag/v0.15.0)
- [vLLM v0.14.1 Release](https://github.com/vllm-project/vllm/releases/tag/v0.14.1)

### Documentation
- [vLLM Engine Arguments](https://docs.vllm.ai/en/stable/configuration/engine_args/)
- [vLLM Pooling Models](https://docs.vllm.ai/en/stable/models/pooling_models/)
- [vLLM V1 Architecture](https://blog.vllm.ai/2025/01/27/v1-alpha-release.html)

### Previous Migrations
- [MIGRATION_VLLM_0.14.1.md](MIGRATION_VLLM_0.14.1.md) - vLLM 0.11.2 → 0.14.1 migration
- [CHANGELOG_S3_RUNAI.md](CHANGELOG_S3_RUNAI.md) - S3/RunAI streamer support

## Conclusion

The migration from vLLM 0.14.1 to 0.15.1 is **straightforward and low-risk**. No code changes are required, only dependency version bumps. The primary benefits are:

1. **Significant performance improvements** (4x faster torch.compile)
2. **Security fixes** (CVE patches)
3. **Bug fixes** (prefix cache, speculative decoding)
4. **New features** (enhanced API, more model support)

**Recommendation:** Proceed with migration. Focus testing on embeddings and reranking endpoints to verify PoolingParams changes are transparent.
