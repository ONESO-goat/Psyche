# Contradiction Layer

## Overview

The **Contradiction Layer** is a major cognitive subsystem within **Psyche** responsible for challenging, qualifying, refining, and potentially rejecting theories produced by other cognitive systems.

The purpose of the Contradiction Layer is not to simply determine whether a statement is "true" or "false."

Instead, it asks:

> **"What information, evidence, context, or alternative explanation could make this theory incomplete, inaccurate, or misleading?"**

A General may produce a highly confident theory, but confidence alone does not make the theory correct. The Contradiction Layer provides Psyche with an independent mechanism for questioning its own conclusions.

---

## Core Concept

Psyche treats generated conclusions as **theories or hypotheses**, rather than automatically treating them as absolute facts.

For example:

```text
General:

"Apples are beneficial to human health."

            ↓

Contradiction Layer:

"Potentially relevant counter-information exists.
The statement may depend on context, quantity,
individual circumstances, or other factors."

            ↓

Refined Theory:

"Apples may provide nutritional benefits, but
the effects of consuming them can depend on
context and individual circumstances."
```

The example above is intentionally simplified. The Contradiction Layer should rely on retrieved knowledge and evidence rather than inventing objections.

---

# Responsibilities

The Contradiction Layer may be responsible for:

* Detecting conflicts with known information
* Finding counterexamples
* Identifying missing context
* Identifying unsupported assumptions
* Finding alternative explanations
* Comparing competing theories
* Evaluating evidence supporting a theory
* Evaluating evidence opposing a theory
* Detecting internal logical inconsistencies
* Reducing confidence when appropriate
* Requesting additional information when evidence is insufficient
* Refining theories rather than unnecessarily rejecting them

The system should **challenge theories, not automatically destroy them.**

---

# Theory Evaluation

A theory should be treated as an object rather than simply a string of text.

Conceptually:

```text
Theory
├── Statement
├── Source
├── Supporting Evidence
├── Contradicting Evidence
├── Context
├── Associations
├── Assumptions
├── Confidence
└── Unknowns
```

The Contradiction Layer can then evaluate the theory against Psyche's available knowledge.

---

# Possible Outcomes

The Contradiction Layer should not be limited to `true` or `false`.

Possible outcomes include:

### Supported

The available information does not reveal meaningful contradictions.

```text
THEORY → SUPPORTED
```

### Qualified

The theory may be reasonable but requires additional conditions or context.

```text
THEORY
  ↓
"Generally true, but..."
```

### Competing Explanation

Another explanation may account for the available evidence equally well or better.

```text
THEORY A
     ↕
THEORY B
```

### Contradicted

Available evidence meaningfully conflicts with the theory.

```text
THEORY → CONTRADICTED
```

### Insufficient Evidence

Psyche does not have enough information to make a meaningful determination.

```text
THEORY → INSUFFICIENT INFORMATION
```

This distinction is important because **absence of evidence should not automatically become evidence of contradiction.**

---

# Relationship With Generals

Generals are responsible for **generating theories**.

The Contradiction Layer is responsible for **challenging those theories**.

Conceptually:

```text
                    INPUT
                      ↓
                   Retrieval
                      ↓
                   General
                      ↓
               Theory Generated
                      ↓
          ┌───────────────────────┐
          │   CONTRADICTION LAYER │
          └───────────────────────┘
                      ↓
        ┌─────────────┼─────────────┐
        ↓             ↓             ↓
     Support       Qualify       Reject
        │             │             │
        └─────────────┼─────────────┘
                      ↓
              Theory Refinement
                      ↓
                 Psyche Core
```

The Contradiction Layer should therefore function as an **independent cognitive perspective** rather than simply becoming another prompt attached to every General.

---

# Knowledge Requirements

The Contradiction Layer may eventually require access to a substantial portion of Psyche's knowledge infrastructure.

Potential information sources include:

* General knowledge
* Structured SQL data
* Vector databases
* Memory retrieval
* Associations
* Previous theories
* Previous contradictions
* Context
* External knowledge
* Evidence metadata

This means the Contradiction Layer may eventually become one of Psyche's largest cognitive systems.

---

# RAG Integration

The Contradiction Layer should be capable of performing its own retrieval.

Instead of only asking:

```text
"What information supports this theory?"
```

it should also ask:

```text
"What information challenges this theory?"
```

Conceptually:

```text
Theory
  ↓
Retrieve Relevant Knowledge
  ↓
Retrieve Related Associations
  ↓
Retrieve Potential Counterexamples
  ↓
Compare Evidence
  ↓
Evaluate Theory
```

This creates a different retrieval objective from ordinary RAG.

Normal RAG attempts to find information **relevant to a query**.

Contradiction-oriented retrieval attempts to find information **relevant to challenging a hypothesis**.

---

# Associations

Associations are especially important to contradiction detection.

A contradiction may not be directly connected to the original theory.

For example:

```text
Theory
  ↓
Topic A
  ↓
Association B
  ↓
Related Knowledge C
  ↓
Potential Contradiction
```

Therefore, contradiction retrieval should eventually be capable of controlled association expansion rather than relying exclusively on semantic similarity.

---

# Self-Correction

The ultimate purpose of the Contradiction Layer is to allow Psyche to **correct and refine its own reasoning**.

Example:

```text
General A:
    "Theory X"

Contradiction Layer:
    "Evidence Y conflicts with X."

General A:
    "Revised Theory X."

Contradiction Layer:
    "Conflict reduced, but uncertainty remains."

Psyche:
    "Final theory is X', with moderate confidence."
```

This creates a feedback loop:

```text
Generate
   ↓
Challenge
   ↓
Refine
   ↓
Challenge Again
   ↓
Accept / Reject / Remain Uncertain
```

---

# Design Philosophy

The Contradiction Layer should follow several principles.

### 1. Challenge, Don't Argue

The purpose is not to disagree with Generals.

Its purpose is to identify meaningful weaknesses.

### 2. Evidence Over Intuition

A contradiction should ideally be supported by retrievable information, logical reasoning, or a demonstrable inconsistency.

### 3. Exceptions Matter

A single exception does not necessarily invalidate a theory.

It may instead indicate that the theory requires additional conditions.

### 4. Uncertainty Is Valid

If Psyche cannot determine whether a theory is correct, it should be able to represent uncertainty rather than inventing an answer.

### 5. The System Can Be Wrong

The Contradiction Layer itself is not an oracle.

Its conclusions are also subject to uncertainty, incomplete knowledge, and incorrect reasoning.

Therefore:

```text
General → Can Be Wrong
Contradiction Layer → Can Be Wrong
Psyche → Must Represent Uncertainty
```

---

# Future Architecture

The initial implementation may be relatively simple.

The long-term architecture could evolve toward:

```text
                         PSYCHE
                            │
             ┌──────────────┼──────────────┐
             │              │              │
          Generals        Memory      Knowledge
             │              │              │
             └──────────────┼──────────────┘
                            ↓
                    Theory Generation
                            ↓
                 ┌────────────────────┐
                 │ CONTRADICTION LAYER│
                 ├────────────────────┤
                 │ Evidence Retrieval │
                 │ Association Search │
                 │ Counterexamples    │
                 │ Logic Evaluation   │
                 │ Context Analysis   │
                 │ Theory Comparison  │
                 └─────────┬──────────┘
                           ↓
                    Theory Refinement
                           ↓
                    Confidence Update
                           ↓
                       Psyche Core
```

---

# Long-Term Goal

The Contradiction Layer exists to give Psyche something that a single generative system naturally lacks:

> **A dedicated mechanism for questioning its own conclusions.**

Rather than building a system that only asks:

> "What is the answer?"

Psyche should eventually be capable of asking:

> "Why do I believe this?"

> "What evidence supports it?"

> "What evidence challenges it?"

> "What am I assuming?"

> "What information might I be missing?"

> "Is there another explanation?"

> "Should my theory be revised?"

The Contradiction Layer is therefore intended to become a fundamental component of Psyche's cognitive architecture, providing **critical reasoning, theory refinement, and epistemic uncertainty** alongside the generative capabilities of the Generals.
