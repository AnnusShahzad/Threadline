import cytoscape, { type Core } from "cytoscape";

const ENTITY_COLOUR = "#38bdf8";
const EDGE_COLOUR = "#64748b";
const LABEL_COLOUR = "#e2e8f0";

/**
 * Mount an empty canvas. Entities and edges arrive from the backend in later commits, so
 * this only fixes the visual vocabulary the graph will use.
 */
export function mountGraph(container: HTMLElement): Core {
  return cytoscape({
    container,
    elements: [],
    style: [
      {
        selector: "node",
        style: {
          "background-color": ENTITY_COLOUR,
          label: "data(label)",
          color: LABEL_COLOUR,
          "font-size": 10,
        },
      },
      {
        selector: "edge",
        style: {
          "line-color": EDGE_COLOUR,
          "target-arrow-color": EDGE_COLOUR,
          "target-arrow-shape": "triangle",
          "curve-style": "bezier",
        },
      },
    ],
    layout: { name: "grid" },
  });
}
