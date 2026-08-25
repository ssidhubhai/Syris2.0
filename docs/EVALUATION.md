# EVALUATION.md — Benchmark and QA System

## 1. Why

The AI cannot be judged only by demos. Every meaningful architecture/prompt/model change must be tested against a fixed benchmark.

## 2. Initial benchmark

Recommended starting set:
- 20 Physics questions;
- 20 Mathematics questions;
- 20 Chemistry questions;
- 10 image questions;
- 10 handwritten attempts;
- 10 Hinglish doubts;
- 10 hint-only tasks.

These can overlap; the point is coverage, not the exact count.

## 3. Benchmark categories

### Correctness
Did the system reach a correct result?

### Reasoning linkage
Can the student see why each step follows?

### Presentation selection
Did it choose a visual only when useful?

### Visual correctness
Does the diagram/graph/annotation match the intended semantics?

### Reference usability
Can the student navigate to referenced equations/steps?

### Language
Is Hinglish natural and technically precise?

### Concision
Did it avoid unnecessary content?

### Layout
Is the page readable without cognitive overload?

### Reliability
Was the output valid and recoverable under provider failures?

## 4. Suggested scoring

Example starting weights:
- correctness: 30%
- reasoning/step linkage: 20%
- presentation usefulness: 15%
- visual correctness: 10%
- language: 10%
- schema reliability: 5%
- latency: 5%
- resilience: 5%

These weights are adjustable after real student testing.

## 5. Golden cases

Every regression found in real usage should become a benchmark case.

## 6. Model certification

A new model/provider must pass the benchmark before entering the routing pool.

## 7. Human review

A subset of the benchmark should always be reviewed manually by a JEE-capable reviewer/student because automated metrics cannot fully measure pedagogical quality.
