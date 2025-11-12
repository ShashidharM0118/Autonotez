import * as React from "react";
import Card from "./Card";

export function SummaryCard({ title, items }: { title: string; items: string[] }) {
  return (
    <Card title={title}>
      <ul className="list-disc pl-4 text-sm text-subtext">
        {items.map((it, i) => (
          <li key={i} className="mb-1 text-text/90">
            {it}
          </li>
        ))}
      </ul>
    </Card>
  );
}

export default SummaryCard;
