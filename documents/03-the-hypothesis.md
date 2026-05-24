# The Agentic Hierarchy of Needs
## Part III: The Hypothesis

---

### 3.1 Formal Statement

The Agentic Hierarchy of Needs produces a testable hypothesis about agentic software development systems:

**Hypothesis:** In multi-contributor software projects expected to live for meaningful periods — where agents produce a substantial fraction of changes, where the contributor population turns over across the project's lifetime, and where delivery rather than discovery is the primary mode of work — systems that operate with a formally defined rigidity hierarchy will outperform systems that do not. By *outperform* the hypothesis means specifically that such systems will be more correct, more stable, more maintainable, and more scalable across the timescales and contributor counts the hierarchy is designed for. The hierarchy is defined as described in Part II: intent, requirements, and executable contracts established before implementation, with agents prohibited from altering layers at or below the membrane.

The scope qualifier is deliberate. The claim is not that all software in all contexts must be built this way. It is that the conditions under which the hierarchy is necessary are the conditions toward which the field is rapidly moving: agent-driven change rates, larger and more elastic contributor populations, longer system lifetimes, shorter human attention windows per change. Where those conditions do not hold — single-maintainer scripts, exploratory spikes, throwaway prototypes, evaluation of agentic features themselves — the hierarchy's costs may exceed its benefits, and the framework concedes those cases openly. Section 4.4 enumerates them.

More specifically, the hypothesis predicts:

1. **Correctness** — Systems built hierarchy-first will have a lower rate of silent drift between stated intent and implemented behavior, because the membrane provides a continuous executable check.

2. **Stability** — Systems built hierarchy-first will have a lower rate of regression across feature cycles, because all prior contracts are enforced simultaneously on every run.

3. **Scalability** — Systems built hierarchy-first will maintain correctness and stability at larger scale and over longer time horizons than systems built without the hierarchy, because the enforcement mechanism is structural rather than dependent on human vigilance.

4. **Agent safety** — Systems built hierarchy-first allow greater agent autonomy at the upper layers without greater risk, because the membrane constrains the solution space within which agents operate freely.

---

### 3.2 Corollary Predictions

The framework also produces corollary predictions that can be evaluated independently:

**Corollary A — Top-down specification is self-defeating.**
Systems in which designers specify implementation details without first establishing contracts will exhibit higher rates of misalignment between stated requirements and implemented behavior. The more prescriptive the implementation specification without a corresponding contract layer, the greater the eventual divergence.

**Corollary B — The membrane is the leverage point.**
Improvements to agent capability at the implementation, state, or infrastructure layers will produce diminishing returns without a strong contract layer. The bottleneck for system correctness is not agent capability — it is the quality and completeness of the contracts.

**Corollary C — Autonomy without the hierarchy is a liability.**
Increasing agent autonomy in systems without a formal hierarchy will produce faster accumulation of silent errors, not faster correct delivery. Speed of output is not correlated with correctness of output in the absence of the membrane.

---

### 3.3 What Would Falsify This

A framework that cannot be falsified is not a theory — it is an ideology. The following findings would constitute evidence against the hierarchy framework:

- Systems built without a formal contract layer that nonetheless maintain correctness and stability at large scale over long time horizons, by some mechanism other than the one described here.

- Evidence that agents can reliably self-evaluate translation correctness — that is, that an agent can determine, without an external executable check, whether its output satisfies human intent — which would undermine the claim that the membrane is necessary.

- Evidence that the cost of establishing the contract layer (writing tests before implementation) consistently exceeds the benefit in reduced regression and drift, *within the scope conditions stated in the hypothesis*, which would suggest the hierarchy is theoretically correct but practically uneconomical even where the conditions are met.

These falsification conditions are offered in good faith. The framework should be held to them.

---

### 3.4 Anticipated Objections

Two objections come up more often than any others. Both deserve to be addressed in the document itself rather than left for the reader to discover and dismiss alone.

**Counterexamples from human-led projects.** There are well-known long-lived systems — the Linux kernel, SQLite, Postgres — that have maintained correctness and stability at large scale over long horizons without operating in the strict hierarchy described here. They are not counterexamples in the sense this framework cares about. Their primary coordination mechanism is human judgment concentrated in a small number of long-tenured maintainers, supplemented by review culture and, in the case of SQLite, an unusually rigorous test suite. That model works. It works at human speed. It does not generalize to agent-driven change rates, for the reason laid out in Part I: maintainer attention is the bottleneck, and that bottleneck does not scale to the volume of changes an agent-assisted workflow produces. The claim here is not that human-led systems cannot be correct without the hierarchy. The claim is that agent-led systems cannot reliably be, and that running a human-judgment regime at agent speed produces, in practice, abandonment of review.

**Economic conditions.** The hierarchy is not cost-free. Establishing contracts before implementation has a real upfront cost, and the existing literature on test-driven development in human teams shows mixed results on whether that cost pays back across a project's lifetime. The claim here is conditional, not universal. The hierarchy's economics improve as expected system lifetime increases, as contributor turnover increases, and as the agent-driven change rate increases. The break-even is project-dependent. A one-shot script written by one developer who will maintain it alone for a week is overhead under this hierarchy, and the framework does not recommend it for that case. A long-lived system being modified by rotating teams with agents producing a significant share of the changes is the case where the hierarchy is the only mechanism that compounds. Most of the field's current TDD evidence comes from contexts closer to the former than the latter. The strongest economic case for this framework is in contexts where that evidence base is thinnest, which is also where the field is heading fastest.

A related concern about execution cost is worth addressing directly. Running a large test suite continuously sounds expensive in the abstract. In practice, the membrane the framework prefers is built from programmatic tools — vitest, JUnit, pitest, Playwright, and their peers — which execute in a job and are extremely cheap per run. They are invoked when state is being verified, not on every keystroke. A team can build with agents for an hour and then run the suite; or build for a minute and run the suite; the choice is theirs and the cost is bounded by the tooling, not by the agent. The expensive case — running an agent to grade whether a contract was satisfied — is reserved for the fuzzy band of the membrane where nothing programmatic is available. If a team finds itself running model-graded contracts as the default, the question is not whether the framework is too expensive. The question is why the team is using a sports car to deliver food. Push contracts toward programmatic verification first; the cost concern resolves itself.

**Exploratory and discovery work.** The framework is not aimed at spikes, prototypes, research notebooks, one-off scripts, or evaluation of agentic feature sets themselves. In those modes, intent is not stable enough to encode upstream — the point of the work is to discover what intent should be. Requiring contracts before implementation in a spike defeats the spike. AHN is a foundation discipline for delivery, not a method for every interaction with an agent. Teams should be free to operate without the hierarchy when the mode of work is exploration. They should be deliberate about when they cross back into delivery, because that is the boundary at which the hierarchy begins to pay for itself.

**Adversarial robustness and agent safety.** Prompt injection, tool misuse, jailbreaks, exfiltration via tool calls — these are real problems and the framework does not solve them. The membrane is a correctness contract, not a security boundary. Defense-in-depth for agentic systems — capability scoping, allowlists, output filters, sandboxing — is a parallel discipline with its own literature. AHN does not oppose it. It assumes it where the system requires it. A framework that tried to be a hierarchy of needs and a security model simultaneously would be worse at both.

**Coexistence with skills, memory, and protocol layers.** Modern agent platforms expose composable primitives — skills, memory tools, MCP servers, sub-agent orchestration. The framework does not require teams to ignore these. It is consistent with them. A skill is closer to a frozen capability than to a contract, but the contracts that govern its use sit at the membrane the same way any other contract does. Memory primitives reduce the per-session reconstitution cost described in Part I, which is a benefit, not a contradiction. Sub-agent orchestration is a contributor topology, and the membrane is invariant under contributor topology by construction (see §2.7). Teams should use these primitives where they help. The framework's claim is structural: whatever toolchain a team adopts, the contracts must still be derived from intent and inviolable from below, or the system will drift.

**Human-in-the-loop, surgically.** The framework is sometimes read as dismissing human review. It is not. The position is narrower and more specific. Human review applied to every change cannot scale to agent-driven change rates, and treating it as the primary coordination mechanism in an agent-heavy workflow effectively guarantees its abandonment. Surgical HITL — gating dangerous tool calls, approving infrastructure changes, signing off on contract amendments — is the correct pattern and is consistent with the hierarchy. The membrane is what makes HITL surgical possible: when the test suite reports green on every contract, the human does not need to inspect each change. They need to inspect only the changes that move the membrane itself. That is a tractable surface area. Without the membrane, the human is expected to inspect everything, which is precisely the workload that does not scale.

---

*Previous: [Part II — The Framework](02-the-framework.md)*
*Next: [Part IV — Implications](04-implications.md)*
