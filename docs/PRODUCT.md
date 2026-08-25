# PRODUCT.md — V1 Product Specification

## 1. Product statement

An AI-powered JEE study companion that transforms normal AI answers into clear, visually connected, adaptive study explanations.

## 2. Problem

Normal chat AI can provide correct step-by-step answers but often presents them as a long linear transcript. References such as “using the equation above” require scrolling; related equations, diagrams and reasoning are not spatially connected; and the student must mentally reconstruct the teacher's board/notes.

## 3. V1 goal

Remove that presentation gap.

The system should make an answer feel like a carefully prepared teacher solution sheet:
- clear hierarchy;
- linked reasoning;
- contextual diagrams;
- visible transformations;
- labels and annotations;
- compact references;
- persistent context;
- flexible layout;
- no unnecessary decoration.

## 4. Target user behavior

A student may:
- type a question;
- upload a question image;
- upload a handwritten attempt;
- ask a follow-up;
- ask for a specific step/why;
- ask for a concept explanation;
- ask for a solution.

## 5. What V1 is not

- not a full coaching replacement;
- not a chapter-course system;
- not a classroom simulator;
- not primarily a progress-tracking product;
- not a social product;
- not a gamification system.

## 6. Core V1 capabilities

### Input
- text;
- image;
- optional voice later in V1/V1.5 if stable.

### Understanding
- classify user intent;
- parse problem/context;
- parse student attempt when present;
- determine complexity and presentation needs.

### Explanation
- structured natural-language explanation;
- equations;
- derivations;
- contextual visuals;
- annotations;
- connected references;
- adaptive layout.

### Workspace
- full-screen digital paper;
- zoom/pan where useful;
- jump-to-reference;
- focus current step;
- reopen previous session.

### Persistence
- session history;
- messages;
- generated explanation document;
- whiteboard state.

## 7. Success metric

Primary UX metric:

> Can the student understand why the current step follows from the previous step without scrolling back to reconstruct missing context?

Secondary metrics:
- correctness;
- visual usefulness;
- readability;
- low frustration;
- response latency;
- schema reliability.
