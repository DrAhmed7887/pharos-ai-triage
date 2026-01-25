import React, { useState } from 'react';
import { UserPlus, Hash } from 'lucide-react';

export default function PatientRegistration({ onRegister }) {
    const [name, setName] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!name.trim()) return;

        // Generate a simple unique ID (e.g., PT-Timestamp-Random)
        // For better readability: #PT-{random 4 digits}
        const randomId = Math.floor(1000 + Math.random() * 9000);
        const id = `PT-${randomId}`;

        onRegister({ name, id });
    };

    return (
        <div className="max-w-2xl mx-auto bg-white rounded-xl shadow-lg border border-slate-100 overflow-hidden">
            <div className="p-6 bg-gradient-to-r from-blue-600 to-blue-700 text-white flex items-center gap-3">
                <div className="bg-white/20 p-2 rounded-lg">
                    <UserPlus className="w-6 h-6 text-white" />
                </div>
                <div>
                    <h2 className="text-lg font-bold">Patient Registration / تسجيل مريض</h2>
                    <p className="text-blue-100 text-sm">Create a new patient file to start triage.</p>
                </div>
            </div>

            <form onSubmit={handleSubmit} className="p-8 space-y-6">
                <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">Patient Name / اسم المريض</label>
                    <input
                        type="text"
                        autoFocus
                        required
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        className="w-full text-lg rounded-lg border-slate-300 shadow-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 py-3 px-4 border"
                        placeholder="Enter full name..."
                    />
                </div>

                <button
                    type="submit"
                    className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-lg shadow-sm transition-colors flex items-center justify-center gap-2"
                >
                    <Hash className="w-5 h-5" />
                    Generate ID & Start Triage
                </button>
            </form>
        </div>
    );
}
