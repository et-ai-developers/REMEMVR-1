# Performance Optimization for rq_scholar and rq_stats

## Current Performance Issues

### Bottlenecks Identified
1. **WebSearch Volume**: Each agent performs 6-10 WebSearch queries
   - rq_scholar: 3-5 validation + 3-5 challenge queries
   - rq_stats: 3-5 validation + 3-5 challenge queries
   - Total: 12-20 searches per RQ

2. **Estimated Time Impact**
   - WebSearch latency: ~5-10 seconds per query
   - 10 queries × 8 seconds = 80 seconds minimum
   - Plus processing/writing time: ~40-60 seconds
   - Total per agent: **2-3 minutes expected**

3. **Parallel Execution Issues**
   - When running 4 RQs in parallel, WebSearch may throttle/timeout
   - Observed freezing on 7.1.3/7.1.4 during parallel execution

## Optimization Strategies

### Option 1: Reduce WebSearch Queries (Quick Fix)
```yaml
# Modified agent configuration
rq_scholar:
  validation_queries: 2  # Down from 3-5
  challenge_queries: 2   # Down from 3-5
  total: 4              # Down from 6-10

rq_stats:
  validation_queries: 2  # Down from 3-5
  challenge_queries: 2   # Down from 3-5
  total: 4              # Down from 6-10
```

### Option 2: Skip WebSearch for Ch7 (Fastest)
Since Ch7 is predictive validity (well-established methods), we could:
1. Create `rq_scholar_lite` and `rq_stats_lite` agents
2. Remove WebSearch tool entirely
3. Use existing knowledge for validation
4. Run time: ~30 seconds per agent

### Option 3: Batch Processing (Recommended)
1. Run rq_scholar/rq_stats sequentially (not parallel)
2. Avoid WebSearch contention/throttling
3. More reliable completion

### Option 4: Cache WebSearch Results
1. Create shared cache for common queries
2. "multiple regression best practices" → cached
3. "IRT sample size requirements" → cached
4. Reuse across similar RQs

## Recommended Approach for Ch7

Given that Ch7 uses standard regression methods:

1. **Create lite versions** of agents for Ch7:
   - `rq_scholar_ch7` - No WebSearch, focus on internal consistency
   - `rq_stats_ch7` - No WebSearch, validate against known standards

2. **Or modify existing agents** with conditional logic:
   ```
   if chapter == 7:
       max_queries = 2  # Minimal searches
   else:
       max_queries = 6  # Standard searches
   ```

3. **Run sequentially** instead of parallel:
   - Prevents WebSearch timeouts
   - More predictable timing
   - Better error handling

## Expected Performance After Optimization

### Current (per RQ)
- rq_scholar: 2-3 minutes
- rq_stats: 2-3 minutes
- Total: 4-6 minutes

### After Optimization (Option 2 - No WebSearch)
- rq_scholar_lite: 20-30 seconds
- rq_stats_lite: 20-30 seconds
- Total: <1 minute

### After Optimization (Option 1 - Reduced Queries)
- rq_scholar: 1-1.5 minutes
- rq_stats: 1-1.5 minutes  
- Total: 2-3 minutes

## Implementation Decision

For Ch7 specifically, recommend **Option 2** (lite versions without WebSearch) because:
- Ch7 uses well-established statistical methods (multiple regression, hierarchical regression)
- Literature is mature and well-documented
- Faster iteration for 24 remaining RQs
- Can always run full validation later if needed