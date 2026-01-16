import React, { useState } from 'react';
import TriageForm from './components/TriageForm';
import TriageResult from './components/TriageResult';
import PatientList from './components/PatientList';
import { Activity, ClipboardList } from 'lucide-react';

function App() {
  const [currentResult, setCurrentResult] = useState(null);

  return (
    <div className="min-h-screen bg-slate-50 font-sans" dir="ltr">
      <header className="bg-white shadow-sm border-b border-slate-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="bg-blue-600 p-2 rounded-lg">
              <Activity className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-slate-900">ER Triage AI</h1>
              <p className="text-xs text-slate-500">Egyptian Hospitals Edition</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <button
              onClick={() => window.location.reload()}
              className="text-sm font-medium text-blue-600 hover:text-blue-700 flex items-center gap-1"
            >
              <ClipboardList className="w-4 h-4" />
              New Patient
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column: Triage Interface */}
          <div className="lg:col-span-2">
            {!currentResult ? (
              <TriageForm onResult={setCurrentResult} />
            ) : (
              <TriageResult result={currentResult} onReset={() => setCurrentResult(null)} />
            )}
          </div>

          {/* Right Column: Live Dashboard */}
          <div className="lg:col-span-1">
            <PatientList />
          </div>
        </div>
      </main>

      <footer className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 text-center text-slate-400 text-sm">
        <p>Clinical Decision Support Tool - Not a substitute for professional medical judgment.</p>
        <p>Emergency: 123 (Ambulance)</p>
      </footer>
    </div>
  );
}

export default App;
