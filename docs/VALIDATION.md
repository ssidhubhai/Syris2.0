# VALIDATION.md — Reliability and Correctness

## 1. Layers

### Schema validation
Checks shape and required fields.

### Semantic validation
Checks whether output makes sense for the task.

### Deterministic math validation
Use SymPy where applicable.

### Chemistry validation
Use RDKit or other domain tools where applicable, with the limitation that no tool validates every JEE chemistry claim.

### Domain rules
Maintain explicit rules for high-frequency JEE traps/boundary conditions.

### Cross-model verification
Use selectively for difficult/high-risk answers.

## 2. Do not equate agreement with truth

Two or more models agreeing does not prove correctness.
Verification must rely on domain logic, deterministic checks, source-grounded data, or an independent verification path when applicable.

## 3. Confidence

The system should preserve uncertainty rather than forcing false certainty.
Low-confidence/high-risk outputs may be flagged for verification or a cautious response.

## 4. Known limitations

No system can guarantee 100% correctness across all JEE questions, messy handwriting, ambiguous diagrams, or advanced multi-concept chemistry/physics. The architecture should reduce risk, detect common classes of error, and make recovery possible.
