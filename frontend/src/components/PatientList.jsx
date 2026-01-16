import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Users, Clock, AlertTriangle } from 'lucide-react';

export default function PatientList() {
    const [patients, setPatients] = useState([]);
    const [loading, setLoading] = useState(true);

    const fetchPatients = async () => {
        try {
            const res = await axios.get('http://localhost:8000/patients');
            setPatients(res.data);
        } catch (err) {
            console.error("Failed to fetch patients", err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchPatients();
        // Poll every 5 seconds for updates
        const interval = setInterval(fetchPatients, 5000);
        return () => clearInterval(interval);
    }, []);

    const getLevelColor = (level) => {
        switch (level) {
            case 1: return "bg-red-100 text-red-800 border-red-200";
            case 2: return "bg-orange-100 text-orange-800 border-orange-200";
            case 3: return "bg-yellow-100 text-yellow-800 border-yellow-200";
            case 4: return "bg-green-100 text-green-800 border-green-200";
            case 5: return "bg-blue-100 text-blue-800 border-blue-200";
            default: return "bg-slate-100 text-slate-800";
        }
    };

    return (
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
            <div className="p-4 border-b border-slate-100 bg-slate-50 flex items-center justify-between">
                <h3 className="font-semibold text-slate-700 flex items-center gap-2">
                    <Users className="w-4 h-4" /> Recent Patients / المرضى الحاليين
                </h3>
                <span className="text-xs text-slate-400 flex items-center gap-1">
                    <Clock className="w-3 h-3" /> Live Updates
                </span>
            </div>

            <div className="divide-y divide-slate-100">
                {loading && <div className="p-4 text-center text-sm text-slate-500">Loading...</div>}

                {!loading && patients.length === 0 && (
                    <div className="p-8 text-center text-slate-400 text-sm">No patients recorded yet.</div>
                )}

                {patients.map(patient => (
                    <div key={patient.id} className="p-4 hover:bg-slate-50 transition-colors flex items-center justify-between">
                        <div className="space-y-1">
                            <div className="flex items-center gap-2">
                                <span className={`px-2 py-0.5 rounded text-xs font-bold uppercase border ${getLevelColor(patient.triage_level)}`}>
                                    Level {patient.triage_level}
                                </span>
                                <span className="text-sm font-medium text-slate-900">
                                    {patient.gender === 'male' ? 'Male' : 'Female'}, {patient.age}y
                                </span>
                            </div>
                            <p className="text-xs text-slate-500 line-clamp-1 max-w-[200px] sm:max-w-xs" title={patient.chief_complaint}>
                                {patient.chief_complaint}
                            </p>
                        </div>
                        <div className="text-right">
                            <div className="text-xs font-bold text-slate-700">
                                {new Date(patient.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                            </div>
                            {patient.triage_red_flags && patient.triage_red_flags.length > 0 && (
                                <div className="flex items-center justify-end gap-1 text-[10px] text-red-600 font-medium">
                                    <AlertTriangle className="w-3 h-3" /> Red Flag
                                </div>
                            )}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
