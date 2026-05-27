interface Props { score: number }

export function RiskBadge({ score }: Props) {
  const color = score >= 70
    ? 'bg-red-100 text-red-700 border-red-200'
    : score >= 40
    ? 'bg-yellow-100 text-yellow-700 border-yellow-200'
    : 'bg-green-100 text-green-700 border-green-200'

  const label = score >= 70 ? 'High risk'
              : score >= 40 ? 'Medium risk'
              : 'Safe'

  return (
    <span className={`inline-flex items-center gap-1 px-2 py-0.5
      text-xs font-medium rounded border ${color}`}>
      {label} · {score}/100
    </span>
  )
}