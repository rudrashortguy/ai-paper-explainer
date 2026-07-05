import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import ErrorBoundary from './ErrorBoundary';
import Uploader from './Uploader';
import SummaryDisplay from './SummaryDisplay';
import { useStore } from './store';
import apiClient from './apiClient';

function App() {
  const [summary, setSummary] = useState(null);
  const { darkMode, toggleDarkMode } = useStore();

  const mutation = useMutation({
    mutationFn: async (file) => {
      const form = new FormData();
      form.append('file', file);
      const res = await apiClient.post('/upload', form);
      return res.data;
    },
    onSuccess: setSummary,
  });

  return (
    <ErrorBoundary>
      <div className={darkMode ? 'dark' : ''}>
        <div className="min-h-screen bg-[#0A2463] p-6 text-white">
          <header className="mx-auto mb-8 flex max-w-3xl items-center justify-between">
            <h1 className="text-3xl font-bold">AI Paper Explainer</h1>
            <button
              onClick={toggleDarkMode}
              className="rounded-lg bg-white/10 px-4 py-2 transition-colors hover:bg-white/20"
            >
              {darkMode ? '\u2600\uFE0F Light' : '\uD83C\uDF19 Dark'}
            </button>
          </header>

          <div className="mx-auto max-w-3xl">
            <Uploader onUpload={(file) => mutation.mutate(file)} />

            {mutation.isPending && (
              <div className="mt-8 text-center">
                <div className="mx-auto mb-2 h-8 w-8 animate-spin rounded-full border-4 border-blue-400 border-t-transparent" />
                <p className="text-gray-300">Analyzing paper...</p>
              </div>
            )}

            {mutation.isError && (
              <div className="mt-8 rounded-lg border border-red-500 bg-red-500/20 p-4">
                <p className="text-red-200">{mutation.error.message}</p>
              </div>
            )}

            {summary && <SummaryDisplay data={summary} />}
          </div>
        </div>
      </div>
    </ErrorBoundary>
  );
}

export default App;
