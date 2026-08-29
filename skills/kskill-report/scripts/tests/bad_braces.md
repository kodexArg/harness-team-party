# fixture: KNOWN-BAD — placeholder braces collide with mermaid node syntax

```mermaid
%%{init: {'theme':'base','fontFamily':"'Nunito',sans-serif"}}%%
flowchart TD
  A([{{INPUT}}]) --> B{{{DECISION_POINT}}}
  B -->|sí| C[{{PATH_A}}]
```
