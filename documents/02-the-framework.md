# The Agentic Hierarchy of Needs
## Part II: The Framework

---

### 2.1 The Core Insight

The missing translation layer exists. It has existed for decades. It is called a **test**.

Not a test as a QA artifact — something written after code to verify it works. A test as a **primary artifact** — something written immediately after requirements, before any code exists, because a test is what a requirement looks like when it has been made executable.

A test takes human intent, expressed as a requirement, and compresses it into a binary signal: pass or fail. It does not interpret. It does not infer. It evaluates the system against a precise, predetermined condition and returns one of two values. This is the only form of human intent that a machine can evaluate without interpretation.

This insight has a corollary that is equally important:

**A test suite is the executable memory of a system's contracts.**

It does not drift. It does not forget. It does not get replaced by a new team member who read the spec differently. It holds every prior contract simultaneously, evaluates all of them on every run, and reports any violation immediately. It is the closest thing software has to a persistent, incorruptible institutional memory.

And for an agent, it is the only reliable signal that work is done. Not "the agent thinks it looks right." Not "the code compiles." Not "a human spot-checked it." The tests pass. All of them. Including every contract established in every prior version of the system.

---

### 2.2 The Hierarchy

Once the translation layer is identified, the full structure of the hierarchy becomes visible. Every software system — and by extension every agentic software development workflow — is organized into layers. These layers differ from each other in one critical dimension: **how much they should be allowed to change, and who or what is allowed to change them.**

The Agentic Hierarchy of Needs orders these layers by rigidity, from most rigid at the base to most malleable at the top. The pyramid shape is deliberate. The base is wide because it bears the weight of everything above it. The apex is narrow because it is the furthest from the foundation and the most freely shaped.

```
            ▲
           /|\
          / | \
         /  |  \
        / INFRA \          ← most agent-autonomous
       /─────────\
      /   STATE   \
     /─────────────\
    / IMPLEMENTATION \
   /─────────────────\
  /     CONTRACTS     \
 /═══════════════════════\  ← The Membrane
/      REQUIREMENTS       \
/─────────────────────────\
/          INTENT           \  ← must originate from human
▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
```

**The six layers, from base to apex:**

| Layer | What It Is | Who Owns It | Rigidity |
|---|---|---|---|
| Intent | What the human wants | Human only | Foundational — must originate from human |
| Requirements | Intent made precise and structured | Human, with agent assistance | Policy-immutable |
| Contracts | Requirements made executable (tests) | Human validates, agent cannot alter | Structurally immutable — the membrane |
| Implementation | Code that satisfies contracts | Agent, within constraints | Malleable |
| State | Data that satisfies implementation | Agent, within schema constraints | Malleable |
| Infrastructure | Environment supporting all above | Agent, near-fully autonomous | Most malleable |

---

### 2.3 The Two Laws

The shape of the hierarchy produces two laws that govern how the system must operate.

**Law I — Autonomy Increases With Altitude**

The higher a layer sits in the pyramid, the more freedom the agent has to make decisions within it. At the base, the agent has no authority — intent must originate from a human. At the apex, the agent operates with near-complete autonomy — infrastructure decisions are almost entirely within agent discretion.

The membrane — the contracts layer — is the hard boundary. Below it, humans are the authority. Above it, agents are the authority. The membrane converts between the two domains. It is the only point in the system where human intent and agent execution meet and can be verified against each other.

This law has an important implication: **agent autonomy is not dangerous at altitude**. An agent making free decisions about infrastructure, state, and implementation is not a risk if those decisions are continuously evaluated against contracts that were established by humans. The contracts constrain the solution space. Within that space, agent autonomy is not only safe — it is the point.

**Law II — You Cannot Enforce Downward Without Grounding Upward**

A designer cannot legitimately specify implementation — what the code should look like, how the API should be structured, what the data schema should be — without first having established intent, requirements, and contracts at the layers below.

If you attempt to build from the top of the pyramid down — specifying implementation without contracts, contracts without requirements, requirements without intent — you are building on no foundation. The upper layers have nothing to be accountable to. The agent has no truth to orient toward. You are generating artifacts that feel correct but have no verifiable relationship to any human need.

This is the failure mode that produces the silent drift described in Part I. The code looks right. The tests, if they exist at all, were written to match the code rather than to encode the requirements. The system does what it was built to do, which may or may not be what the human wanted, and there is no executable mechanism to know the difference.

The law is therefore both descriptive and prescriptive: it describes why top-down specification fails, and it prescribes that designers must resist the temptation to enforce implementation choices artificially when the foundational layers have not been established first.

---

### 2.4 The Maslow Parallel

The analogy to Maslow's hierarchy of needs is instructive and intentional.

Maslow's hierarchy proposes that human needs are ordered by prerequisite — that higher-order needs (esteem, self-actualization) cannot be meaningfully pursued until lower-order needs (physiological, safety) are satisfied. You cannot focus on belonging when you are starving. The lower needs are not less important than the higher ones. They are more important, in the sense that they must come first.

The Agentic Hierarchy of Needs operates on the same logic. Higher layers cannot be meaningfully pursued until lower layers are satisfied.

An agent cannot produce trustworthy implementation without contracts to satisfy. Contracts cannot encode anything meaningful without requirements to derive from. Requirements cannot be precise without intent to ground them. Each layer presupposes the one below it.

The parallel extends further. In Maslow's framework, deficiency at a lower level creates pathological behavior at higher levels — a person whose safety needs are unmet becomes preoccupied with safety in ways that distort all higher-order functioning. In the agentic hierarchy, deficiency at a lower level creates pathological behavior in higher layers as well. An agent operating without contracts produces confident, fluent, plausible-looking implementation that is not accountable to any requirement. An agent operating without clear requirements generates contracts that test the wrong things. The pathology propagates upward.

And as in Maslow's framework, the solution is not to address the symptoms at the higher layers. It is to satisfy the deficiency at the lower layer first.

One caveat. Maslow's hierarchy is empirically contested within psychology — the strict ordering of needs, the universality of the levels, and the predictive power of the model are all genuinely disputed. The analogy here is not borrowing Maslow's empirical claims, only the shape of the argument. Prerequisite-ordered needs are a recognizable structure, and the agentic hierarchy borrows that structure because it is familiar. If Maslow's pyramid were replaced tomorrow by a better model of human motivation, the agentic hierarchy would stand or fall on its own. The parallel is scaffolding, not foundation.

---

### 2.5 The Membrane in Detail

The contracts layer is the most important layer in the hierarchy and deserves elaboration beyond its position in the pyramid.

The membrane is not merely a layer. It is a **translation interface** between two fundamentally different modes of expression.

Below the membrane, everything is human: intent is stated in natural language, requirements are written in structured prose, and both are subject to interpretation, revision, and the limitations of human communication. Above the membrane, everything is machine: code executes deterministically, data conforms to schemas, infrastructure responds to configuration. These two worlds do not naturally speak to each other.

The contracts layer — executable tests — is the only artifact in the system that exists in both worlds simultaneously. A well-written test is readable by humans as a statement of required behavior. It is executable by machines as a binary evaluation of actual behavior. It is the Rosetta Stone of the system: human-readable below, machine-executable above.

This dual nature is what makes the membrane the correct location for the hard boundary between human authority and agent authority. It is the only place where a human can state something and a machine can verify it without any further interpretation required.

The membrane must therefore be treated with corresponding care:

- **It is inviolable from above.** Agents cannot alter contracts. An agent that modifies a test to make it pass has not solved the problem. It has destroyed the translation layer. The membrane no longer represents human intent. It represents agent convenience.

  This does not mean contracts never change. They do. Requirements evolve, stakeholders revise an intention, the product turns a corner — and when that happens, the contract above has to change to match. The mechanism is a **contract amendment**: a deliberate, traceable revision that originates above the membrane and propagates downward, not a tactical edit reaching up from the implementation. An amendment needs an explicit upstream change — revised intent stated, requirement re-derived from it, contract updated to encode the new requirement. The old contract is versioned and superseded, not silently deleted. Whoever inherits the system later can still read the history of what it was supposed to do.

  That distinction is what reconciles "inviolable" with the obvious fact of changing requirements. Agents may *propose* amendments. They may flag that a contract appears to conflict with a new requirement, or surface that a test is constraining the implementation in a way that may no longer reflect intent. They may not *enact* amendments. Enactment is the human's gesture — the act of authoring intent, which by definition cannot be delegated to the system being directed by it. The human originates intent, sits below the contracts layer, and can change a contract from there. But only by walking the change down through the hierarchy in the open. Not by reaching up and editing.

- **It is constructed from below.** Contracts must be derived from requirements. A test that is not traceable to a human requirement is not a contract — it is an assertion about the current state of the code, which is a different and much weaker thing.

- **It accumulates over time.** Every passing test is a frozen contract. The membrane grows with every feature cycle, encoding more and more of the system's intended behavior. This accumulation is the mechanism of the compounding effect described next.

- **It has crisp and fuzzy regions.** Not all intent is expressible as a binary check. Functional correctness usually is. Performance, security posture, accessibility compliance, UX quality, evaluation of agentic features against subjective criteria — these are real contracts and they belong at the membrane, but they evaluate as continuous values gated against thresholds rather than as boolean assertions. A latency budget is a contract. A WCAG audit score with a minimum acceptable value is a contract. An eval harness score, gated at a level the human chose, is a contract. They are still derived from above, still inviolable from below, still executable. They just produce numbers rather than booleans, and the human-set threshold converts the number into a pass/fail signal. The membrane is therefore not a sharp line but a band of varying crispness. The principle — executable, derived from above, inviolable from below — holds along the whole band. The band gets fuzzier as the property being measured gets harder to define, and the human is responsible for setting and revisiting the thresholds. Fuzziness at the membrane is acceptable. Absence of a membrane is not.

- **It defaults to programmatic verification.** Where the contract can be encoded as code-against-code — a unit test, an integration test, a property test, a browser-driven end-to-end check, a mutation test, a benchmarked threshold — that is the default mechanism. Programmatic tests run in a job. They are cheap to execute, fast to run, deterministic in result, and they can be invoked on demand or in CI without any agent in the loop. A team using vitest, JUnit, pitest, Playwright, or any of the dozens of mature testing tools in the field is already operating at the membrane in the form the framework prefers. The fuzzy band — where agent-graded or LLM-graded evaluation is unavoidable — exists for properties that genuinely cannot be encoded any other way. It is the exception, not the rule. A team that finds itself reaching for LLM-graded contracts as the default has typically either misidentified the property being tested or has skipped the work of making the property programmatically checkable. Cost and reliability push the same direction: encode what you can with programmatic tools, and reserve agentic grading for what you must. Tests, in the sense the membrane uses the word, are programmatic first.

---

### 2.6 The Compounding Effect

The most powerful property of the hierarchy — and the one most underappreciated in current discussions of agentic development — is that the system becomes more robust over time automatically, without additional human effort.

The mechanism is simple. Every passing test is a frozen contract. The agent cannot alter it. As the test suite grows across feature cycles, the agent must satisfy an ever-expanding lattice of simultaneous constraints:

```
Cycle 1:   contracts {A}
Cycle 2:   contracts {A, B}
Cycle 3:   contracts {A, B, C}
Cycle n:   contracts {A, B, C, ... n}
```

At each cycle, the agent must satisfy all prior contracts in addition to new ones. It cannot make a change that satisfies the new contract but breaks a prior one, because the membrane will report the breakage immediately and the agent must resolve it.

This has a profound consequence for system integrity over time. In conventional software development, technical debt accumulates because human developers make locally rational decisions that erode global coherence. Nobody holds all prior contracts in their head simultaneously. A change that looks correct in isolation turns out to violate a constraint that was established two years ago and has been quietly forgotten. The violation may go undetected for months.

The agent, by contrast, holds all prior contracts simultaneously on every single run. Not because it has superior memory — but because the membrane holds them. The test suite does not forget. It evaluates every contract, every run, and reports any violation immediately. The agent cannot commit a change that introduces a regression without the membrane detecting it.

The result: each feature cycle produces a system that is simultaneously more capable and more constrained, and these two things are not in tension. The constraints are not a limitation on capability. They are the mechanism by which capability becomes trustworthy. The system does not merely grow. It grows stronger.

One caveat the compounding argument requires, because without it the argument is wrong. The membrane only compounds if it stays coherent, and tests can rot. They can go flaky for reasons unrelated to the behavior they were supposed to assert. They can be over-specified to a particular implementation rather than the behavior, in which case they constrain the wrong thing. They can quietly outlive the requirement that justified them, surviving as passing assertions about features nobody asked for anymore. They can pass for reasons that have nothing to do with what they were supposed to prove. A test suite that is never audited will accumulate noise the same way any artifact does, and a noisy suite is not a membrane. It is a wall of green signals that no longer reliably reports anything.

So the hierarchy requires that the membrane be treated as a living artifact with its own maintenance discipline. Mutation testing, periodic contract audits against current intent, flake budgets, explicit retirement of contracts whose requirements have been formally superseded — none of this is optional polish. It is what the compounding effect charges in exchange for compounding at all. Without it, the suite eventually grows contracts that nobody intended and that nothing depends on, and stops being a membrane. Hygiene is not a side cost. It is the condition the compounding effect runs on.

---

### 2.7 The Membrane as Shared Agreement

The hierarchy is sometimes read as describing the relationship between a single agent and a single human. That reading is too narrow. The framework is about the agreement among an arbitrary number of contributors — human, agent, or any mix of the two — about what is currently true of the system, what is allowed to move, and what is not.

The membrane is the locus of that agreement. It is the artifact that every contributor, regardless of who or what they are, can read and evaluate identically. A team of three humans and two agents, a team of a hundred humans and a thousand agents, a team of one human and ten thousand agents — the topology does not matter to the membrane. The contracts pass or they fail. The interpretation cost is paid once, at the moment the contract is written. Every subsequent contributor inherits the answer.

This is the structural reason the hierarchy scales where human coordination rituals do not. Coordination cost in a team without a shared executable membrane grows roughly with the number of pairs of contributors, because every contributor must ultimately align with every other contributor's mental model. Coordination cost in a team with a shared executable membrane is approximately constant in the number of contributors, because nobody is aligning with anyone else's interpretation. They are aligning with the membrane, which is the same artifact for everyone.

This matters more as agents become the dominant share of contributors. An agent can spawn other agents. A workflow can fork sub-agents to handle parallel sub-problems. The number of agents acting on a system over a given period is not a property of the team's hiring plan — it is a property of the work that needs to be done and the budget available. Human contributors are bounded by hiring. Agent contributors are not. A framework designed around the assumption that contributor count grows slowly will be overrun by a workflow in which contributor count is effectively elastic.

The membrane handles this without modification, because the cost of an additional contributor against a shared executable membrane is approximately zero. The agent reads the contracts. The agent produces work that passes or fails them. The membrane reports the result. No additional coordination overhead is incurred by adding the agent. The same property holds in the other direction: removing an agent, replacing one model with another, swapping the entire agent population for a different one — none of these gestures require the membrane to change. The membrane is invariant under contributor turnover.

There is a deeper observation underneath this. Modern language-model-based agents are, in narrow technical senses, already better than humans at certain classes of problem — specifically, problems that involve finding non-obvious connections among a large number of weakly-related constraints. The same property that makes large models good at translation, code synthesis, and pattern completion at scale makes them effective at filling in implementation that satisfies a dense lattice of contracts. They are the **stockfish of software engineering**: tireless, pattern-rich, weak at originating goals but exceptional at satisfying constraints once goals are made explicit.

The framework is the answer to what humans should do when working with that kind of contributor. The human is not competing with the agent at the implementation layer. That contest is already lost in narrow technical terms and is increasingly lost more broadly. The human's lever is the layers below the membrane: stating intent, deriving requirements, encoding contracts. From there, the agent does the work the agent is good at — synthesizing implementation that satisfies the constraints the human has fixed. The hierarchy makes that division of labor explicit, durable, and verifiable. It is what allows the team to scale into populations of agents without losing the thread of what the system is supposed to be.

---

### 2.8 Degrees of Freedom: The Design Primitive

The membrane insight leads directly to a powerful design primitive: **you control agent behavior by deciding what is frozen**.

Tests are always frozen. But you can extend the frozen set to include other artifacts:

- Freeze the **data schema** → agent must bend the API and frontend to fit the schema
- Freeze the **API contract** → agent must bend the data layer and frontend to fit the contract
- Freeze the **frontend behavior** → agent must bend the data and API to fit the UI
- Freeze **any combination** → agent must satisfy all frozen constraints simultaneously

What you freeze defines the shape of the solution space. The agent fills whatever remains unfrozen to satisfy all frozen constraints simultaneously.

This is not telling the agent what to do. This is telling the agent what cannot move, and letting it find what can. The agent is not executing instructions. It is solving a constraint satisfaction problem, and the frozen artifacts are the constraints.

This is a fundamentally more powerful way to direct agent behavior than writing detailed implementation instructions, because it is self-enforcing. You do not need to monitor whether the agent followed your instructions. The frozen artifacts enforce themselves — if the agent violates them, tests fail.

---

### 2.9 The Dissonance Resolution Property

Human developers experience dissonant requirements as a blocking problem. If the data schema says one thing and the API returns another and the frontend expects a third, a human stops and asks for clarification. The conflicting constraints feel irreconcilable.

Agents do not experience dissonance the same way.

An agent with a frozen test, a frozen data schema, a mutable API, and a mutable frontend does not see a conflict. It sees an optimization problem: what shape does the API need to take so that this data schema produces a passing test result through this frontend? It searches for the connective tissue — the D that cleanly follows from A, B, and C — because that is precisely what the underlying mechanism of large language models does at scale.

LLMs are next-token predictors trained on the overwhelming regularity of human-produced artifacts. Given a set of constraints, they are extremely good at finding the completion that satisfies them — even when those constraints appear, from a human perspective, to point in different directions.

This means that the more frozen constraints you give an agent, the more directed its search becomes. You are not limiting the agent by adding constraints. You are reducing its search space and increasing the probability that its output is correct.

One clarification, because this can otherwise read as a contradiction with the law that implementation specification must not precede contract establishment. Freezing a data schema, an API shape, or a frontend behavior is legitimate when the frozen artifact is itself acting as a contract — when it encodes a derived requirement that an intent above it called for. It is illegitimate when it is an implementation preference being smuggled in without a requirement backing it. The test is whether the freeze is traceable. Can you point at the intent and requirement above this frozen artifact that it exists to satisfy? If yes, the freeze is a contract in a different costume, and it belongs at the membrane. If no, the freeze is exactly the top-down specification failure mode Law II forbids, just dressed up as constraint. Same gesture, opposite valence, distinguishable only by what sits above it.

---

### 2.10 Layers as Roles, Not Files

The pyramid is a useful diagram and a misleading one. It implies that any given artifact in a system sits on exactly one layer — that there is a contracts folder, an implementation folder, an infrastructure folder, and the architectural job is to put each file in the right one.

That is not how real systems decompose, and it is not what the hierarchy is describing.

The layers are roles, not file locations. A single artifact can play different roles depending on which concern is looking at it. A Kubernetes manifest is infrastructure to the team building the application running inside it; it is a contract to the platform team responsible for making that environment reliable. A database schema is implementation to the team writing the migration that produces it; it is a contract to every downstream service that reads from it. A frontend behavior is implementation to the engineer writing the component; it is a contract to the test suite that asserts the user-visible behavior on behalf of the requirement above it. The same file plays different roles for different concerns, simultaneously, without contradiction.

Rigidity attaches to the role, not the artifact. A schema can be malleable in one direction and inviolable in another at the same time. The hierarchy is asking, for any given change being proposed: what role is this artifact playing for the concern at hand, and what altitude does that role sit at? The answer determines who is allowed to change it, by what process, and against what authority. Treating layers as folders forces every artifact into a single bucket and then loses the distinctions that actually matter. Treating layers as roles preserves them.

---

*Previous: [Part I — The Problem](01-the-problem.md)*
*Next: [Part III — The Hypothesis](03-the-hypothesis.md)*
