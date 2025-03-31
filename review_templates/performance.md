# Performance-Related Code Review Template

## Algorithmic Efficiency
- [ ] Time complexity is reasonable for the task
- [ ] Space complexity is reasonable for the task
- [ ] No unnecessarily nested loops
- [ ] Efficient data structures are used

## Resource Usage
- [ ] Memory usage is optimized
- [ ] No memory leaks
- [ ] Resources are properly released
- [ ] Connection pooling used where appropriate

## Database Interactions
- [ ] Queries are optimized
- [ ] Appropriate indexes are defined
- [ ] N+1 query problems avoided
- [ ] Batch operations used when appropriate
- [ ] Pagination implemented for large result sets

## Caching
- [ ] Caching strategy is appropriate
- [ ] Cache invalidation is properly handled
- [ ] Cache hit ratios are measured

## Network Optimization
- [ ] Number of network calls minimized
- [ ] Payload sizes are reasonable
- [ ] Data compression used where appropriate
- [ ] Asynchronous calls used where appropriate

## UI Performance
- [ ] Rendering optimizations implemented
- [ ] Minimal DOM manipulations
- [ ] Asset sizes are optimized
- [ ] Lazy loading used where appropriate

## Concurrency
- [ ] Thread safety considered
- [ ] Deadlocks and race conditions addressed
- [ ] Parallelism opportunities utilized

## Measurement
- [ ] Performance metrics are captured
- [ ] Performance bottlenecks are identified
- [ ] Benchmarks exist for critical paths