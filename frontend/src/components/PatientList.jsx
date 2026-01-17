import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Users, Clock, AlertTriangle, Eye, X, Activity } from 'lucide-react';
import { AnimatePresence, motion } from 'framer-motion';

const API_URL = 'http://localhost:8000';

export default function PatientList() {
    const [patients, setPatients] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedPatient, setSelectedPatient] = useState(null);
    const [showAll, setShowAll] = useState(false);

    const fetchPatients = async () => {
        try {
            const res = await axios.get(`${API_URL}/patients?limit=${showAll ? 100 : 10}`);
            setPatients(res.data);
        } catch (err) {
            console.error("Failed to fetch patients", err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchPatients();
        const interval = setInterval(fetchPatients, 5000);
        return () => clearInterval(interval);
    }, [showAll]);

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
        <>
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden flex flex-col h-full max-h-[800px]">
                <div className="p-4 border-b border-slate-100 bg-slate-50 flex items-center justify-between sticky top-0 z-10">
                    <h3 className="font-semibold text-slate-700 flex items-center gap-2">
                        <Users className="w-4 h-4" /> {showAll ? 'All Patients History' : 'Recent Patients'}
                    </h3>
                    <button
                        onClick={() => setShowAll(!showAll)}
                        className="text-xs text-blue-600 hover:text-blue-800 font-medium underline"
                    >
                        {showAll ? 'Show Recent Only' : 'View All History'}
                    </button>
                </div>

                <div className="overflow-y-auto flex-1 divide-y divide-slate-100">
                    {loading && <div className="p-4 text-center text-sm text-slate-500">Loading...</div>}

                    {!loading && patients.length === 0 && (
                        <div className="p-8 text-center text-slate-400 text-sm">No patients recorded yet.</div>
                    )}

                    {patients.map(patient => (
                        <div
                            key={patient.id}
                            onClick={() => setSelectedPatient(patient)}
                            className="p-4 hover:bg-slate-50 cursor-pointer transition-colors flex items-center justify-between group"
                        >
                            <div className="space-y-1">
                                <div className="flex items-center gap-2">
                                    <span className={`px-2 py-0.5 rounded text-xs font-bold uppercase border ${getLevelColor(patient.triage_level)}`}>
                                        Level {patient.triage_level}
                                    </span>
                                    <span className="text-sm font-medium text-slate-900">
                                        {patient.gender === 'male' ? 'M' : 'F'} / {Math.round(patient.age)}y
                                    </span>
                                </div>
                                <p className="text-xs text-slate-500 line-clamp-1 max-w-[180px]" title={patient.chief_complaint}>
                                    {patient.chief_complaint}
                                </p>
                            </div>
                            <div className="text-right">
                                <div className="text-xs font-bold text-slate-700">
                                    {new Date(patient.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                </div>
                                {patient.triage_red_flags && patient.triage_red_flags.length > 0 ? (
                                    <div className="flex items-center justify-end gap-1 text-[10px] text-red-600 font-medium">
                                        <AlertTriangle className="w-3 h-3" /> Warning
                                    </div>
                                ) : (
                                    <div className="opacity-0 group-hover:opacity-100 transition-opacity text-[10px] text-blue-500 font-medium flex items-center justify-end gap-1">
                                        View <Eye className="w-3 h-3" />
                                    </div>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Detail Modal */}
            <AnimatePresence>
                {selectedPatient && (
                    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm" onClick={() => setSelectedPatient(null)}>
                        <motion.div
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.95 }}
                            className="bg-white rounded-2xl shadow-2xl w-full max-w-lg overflow-hidden"
                            onClick={e => e.stopPropagation()}
                        >
                            <div className={`p-6 text-white bg-gradient-to-r ${selectedPatient.triage_level === 1 ? 'from-red-600 to-red-700' : selectedPatient.triage_level === 2 ? 'from-orange-500 to-orange-600' : selectedPatient.triage_level === 3 ? 'from-yellow-500 to-yellow-600' : selectedPatient.triage_level === 4 ? 'from-green-500 to-green-600' : 'from-blue-500 to-blue-600'}`}>
                                <div className="flex justify-between items-start mb-4">
                                    <div>
                                        <h2 className="text-xl font-bold">Patient Details</h2>
                                        <p className="text-white/80 text-sm">ID: #{selectedPatient.id}</p>
                                    </div>
                                    <button onClick={() => setSelectedPatient(null)} className="p-1 hover:bg-white/20 rounded-full transition-colors">
                                        <X className="w-6 h-6" />
                                    </button>
                                </div>
                                <div className="flex gap-4 text-sm font-medium">
                                    <div className="bg-white/20 px-3 py-1 rounded-lg backdrop-blur-md">
                                        {selectedPatient.gender === "male" ? "Male" : "Female"}, {selectedPatient.age} Years
                                    </div>
                                    <div className="bg-white/20 px-3 py-1 rounded-lg backdrop-blur-md">
                                        {new Date(selectedPatient.created_at).toLocaleString()}
                                    </div>
                                </div>
                            </div>

                            <div className="p-6 space-y-6 max-h-[70vh] overflow-y-auto">
                                {/* Complaint */}
                                <section>
                                    <h3 className="text-xs font-bold uppercase text-slate-500 mb-2">Chief Complaint</h3>
                                    <p className="text-slate-900 bg-slate-50 p-3 rounded-lg border border-slate-100">
                                        {selectedPatient.chief_complaint}
                                    </p>
                                </section>

                                {/* Vitals */}
                                <section>
                                    <h3 className="text-xs font-bold uppercase text-slate-500 mb-2 flex items-center gap-1">
                                        <Activity className="w-3 h-3" /> Vitals Recorded
                                    </h3>
                                    <div className="grid grid-cols-3 gap-3">
                                        {Object.entries(selectedPatient.vitals || {}).map(([key, val]) => (
                                            val && (
                                                <div key={key} className="bg-slate-50 p-2 rounded border border-slate-100 text-center">
                                                    <div className="text-[10px] text-slate-500 uppercase">{key}</div>
                                                    <div className="font-mono font-bold text-slate-800">{val}</div>
                                                </div>
                                            )
                                        ))}
                                    </div>
                                </section>

                                {/* Triage Decision */}
                                <section>
                                    <h3 className="text-xs font-bold uppercase text-slate-500 mb-2">Triage Analysis</h3>
                                    <div className="space-y-3">
                                        <div className="flex items-center gap-2">
                                            <div className={`w-3 h-3 rounded-full ${selectedPatient.triage_level === 1 ? 'bg-red-500' : selectedPatient.triage_level === 2 ? 'bg-orange-500' : selectedPatient.triage_level === 3 ? 'bg-yellow-400' : selectedPatient.triage_level === 4 ? 'bg-green-500' : 'bg-blue-500'}`} />
                                            <span className="font-bold text-slate-900">{selectedPatient.triage_label_en} / {selectedPatient.triage_label_ar}</span>
                                        </div>

                                        <div className="space-y-2">
                                            {selectedPatient.triage_reasoning?.map((r, i) => (
                                                <div key={i} className="flex items-start gap-2 text-sm text-slate-600">
                                                    <span className="mt-1.5 w-1 h-1 rounded-full bg-slate-400 shrink-0" />
                                                    {r}
                                                </div>
                                            ))}
                                        </div>

                                        {selectedPatient.triage_red_flags?.length > 0 && (
                                            <div className="mt-2 text-xs text-red-600 bg-red-50 p-2 rounded border border-red-100">
                                                <span className="font-bold">🚩 Red Flags:</span> {selectedPatient.triage_red_flags.join(", ")}
                                            </div>
                                        )}
                                    </div>
                                </section>
                            </div>
                        </motion.div>
                    </div>
                )}
            </AnimatePresence>
        </>
    );
}
