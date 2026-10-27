import { fetchHealth } from "./api";
import { mountGraph } from "./canvas";
import "./styles.css";

const graphContainer = document.querySelector<HTMLElement>("#graph");
const statusLine = document.querySelector<HTMLElement>("#status");

if (graphContainer === null || statusLine === null) {
  throw new Error("index.html is missing #graph or #status");
}

mountGraph(graphContainer);
void reportBackendStatus(statusLine);

async function reportBackendStatus(element: HTMLElement): Promise<void> {
  try {
    const health = await fetchHealth();
    element.textContent = `Backend ${health.status} · database ${health.database}`;
    element.dataset["state"] = "ok";
  } catch (error) {
    element.textContent = error instanceof Error ? error.message : "Backend unreachable";
    element.dataset["state"] = "error";
  }
}
