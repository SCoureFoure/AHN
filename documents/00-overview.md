# The Agentic Hierarchy of Needs
## A Theoretical Framework for Scalable Human-Agent Software Development

---

## Preface

This document is a theoretical framework, not an implementation guide. It argues from first principles that agentic software development — the use of AI agents to autonomously produce, modify, and maintain software systems — has a structural ceiling when practiced without a formal hierarchy of authority between human intent and agent execution. It proposes that ceiling can be removed, and autonomous agent behavior can be made safe and scalable, by organizing the layers of a software system into a rigidity hierarchy modeled on a simple principle borrowed from psychology:

**Higher-order needs cannot be meaningfully pursued until lower-order needs are satisfied.**

The framework presented here is called the **Agentic Hierarchy of Needs**.

**A note on scope.** This framework is aimed at one specific class of work: multi-contributor software projects, expected to live for meaningful periods, in which agents are an integral part of the delivery workflow rather than an occasional accelerant. It is not aimed at exploratory spikes, one-off scripts, research notebooks, prototypes whose purpose is to discover what should be built, or the evaluation of agentic feature sets themselves. Those are legitimate and distinct modes of work, and they have their own disciplines. The Agentic Hierarchy of Needs is the foundation style for projects that need to remain coherent across many contributors — human and agent — over time horizons where institutional memory would otherwise erode. Section 4.4 returns to the question of what this framework is explicitly not for.

---

## Document Index

This framework is split across four documents. Read in order.

| File | Contents |
|---|---|
| `01-the-problem.md` | Why agentic development as currently practiced has a structural ceiling. The human coordination problem. Institutional memory failure. Why current solutions are insufficient. |
| `02-the-framework.md` | The hierarchy. The pyramid. The two laws. The Maslow parallel. The membrane. The compounding effect. |
| `03-the-hypothesis.md` | Formal hypothesis. Specific predictions. Corollary predictions. Falsification conditions. |
| `04-implications.md` | For designers. For agent systems. For the field. Closing statement. |

---

## The Core Argument in Brief

The dominant agentic development pattern today is:

```
Human states intent → Agent produces code
```

This pattern has no reliable mechanism to verify that the output satisfies the intent. It produces drift — slowly in human teams, rapidly in agent-assisted ones — because there is no executable ground truth for the agent to check against.

The solution is a hierarchy of layers ordered by rigidity:

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

Tests — executable contracts — are the membrane between the human domain and the agent domain. They are the only artifact in a software system that converts human intent into a binary, interpretation-free signal that an agent can reliably orient around.

Agents work above the membrane. Humans own below it. The membrane itself is inviolable.

---

*Theoretical framework developed from first principles. Intended as a foundation document for agentic development practice. Case studies and empirical validation to follow.*
