import Flashcards from './Flashcards';

export default function SummaryDisplay({ data }) {
  return (
    <div className="mt-8 space-y-6">
      <section>
        <h2 className="mb-2 text-xl font-bold">TL;DR</h2>
        <p className="text-gray-200">{data.tldr}</p>
      </section>

      <section>
        <h2 className="mb-2 text-xl font-bold">Beginner Explanation</h2>
        <p className="text-gray-200">{data.beginner_explanation}</p>
      </section>

      {data.key_equations?.length > 0 && (
        <section>
          <h2 className="mb-2 text-xl font-bold">Key Equations</h2>
          <ul className="list-inside list-disc space-y-1 text-gray-200">
            {data.key_equations.map((eq, i) => (
              <li key={i}>
                <code className="rounded bg-white/10 px-2 py-0.5">{eq}</code>
              </li>
            ))}
          </ul>
        </section>
      )}

      {data.flashcards?.length > 0 && <Flashcards cards={data.flashcards} />}

      {data.quiz?.length > 0 && (
        <section>
          <h2 className="mb-2 text-xl font-bold">Quiz</h2>
          {data.quiz.map((q, i) => (
            <div key={i} className="mb-3 rounded-lg bg-white/5 p-4">
              <p className="mb-2 font-medium">
                {i + 1}. {q.question}
              </p>
              {q.options?.map((opt, j) => (
                <label key={j} className="block cursor-pointer py-1">
                  <input
                    type="radio"
                    name={`q${i}`}
                    value={j}
                    className="mr-2"
                  />
                  {opt}
                </label>
              ))}
            </div>
          ))}
        </section>
      )}

      {data.research_gaps?.length > 0 && (
        <section>
          <h2 className="mb-2 text-xl font-bold">Research Gaps</h2>
          <ul className="list-inside list-disc space-y-1 text-gray-200">
            {data.research_gaps.map((g, i) => (
              <li key={i}>{g}</li>
            ))}
          </ul>
        </section>
      )}

      {data.future_work?.length > 0 && (
        <section>
          <h2 className="mb-2 text-xl font-bold">Future Work</h2>
          <ul className="list-inside list-disc space-y-1 text-gray-200">
            {data.future_work.map((f, i) => (
              <li key={i}>{f}</li>
            ))}
          </ul>
        </section>
      )}
    </div>
  );
}
