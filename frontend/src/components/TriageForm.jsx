import React, { useState } from 'react';
import axios from 'axios';
import { Mic, AlertCircle, ChevronRight, Activity } from 'lucide-react';

const API_URL = 'http://localhost:8000';

export default function TriageForm({ onResult }) {
    const [formData, setFormData] = useState({
        age: '',
        gender: 'male',
        chief_complaint_text: '',
        vitals: {
            hr: '',
            rr: '',
            spo2: '',
            temp: '',
            sbp: '',
            dbp: '',
            gcs: 15,
            pain_score: 0
        },
        red_flags: {
            history_cardiac: false,
            history_stroke: false,
            immuno_compromised: false
        }
    });

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [useAI, setUseAI] = useState(false);

    const handleVitalChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            vitals: { ...prev.vitals, [name]: value ? parseFloat(value) : '' }
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        try {
            // Clean data for API
            const payload = {
                ...formData,
                age: formData.age ? parseFloat(formData.age) : 0,
                vitals: {
                    ...formData.vitals,
                    hr: formData.vitals.hr ? parseInt(formData.vitals.hr) : null,
                    rr: formData.vitals.rr ? parseInt(formData.vitals.rr) : null,
                    sbp: formData.vitals.sbp ? parseInt(formData.vitals.sbp) : null,
                    dbp: formData.vitals.dbp ? parseInt(formData.vitals.dbp) : null,
                    spo2: formData.vitals.spo2 ? parseFloat(formData.vitals.spo2) : null,
                    temp: formData.vitals.temp ? parseFloat(formData.vitals.temp) : null,
                }
            };

            const endpoint = useAI ? `${API_URL}/ai-triage` : `${API_URL}/triage`;
            const res = await axios.post(endpoint, payload);
            onResult({ ...res.data, isAI: useAI });
        } catch (err) {
            console.error(err);
            setError("Failed to process triage request. Ensure backend is running.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-2xl mx-auto bg-white rounded-xl shadow-lg border border-slate-100 overflow-hidden">
            <div className="p-6 bg-gradient-to-r from-blue-600 to-blue-700 text-white flex justify-between items-center">
                <div>
                    <h2 className="text-lg font-bold">New Patient Triage / تقييم جديد</h2>
                    <p className="text-blue-100 text-sm">Enter patient data below</p>
                </div>

                {/* AI Toggle */}
                <div className="flex items-center gap-2 bg-blue-800/50 p-1.5 rounded-lg border border-blue-500/50">
                    <span className={`text-xs font-bold ${!useAI ? 'text-white' : 'text-blue-300'}`}>Standard</span>
                    <button
                        type="button"
                        onClick={() => setUseAI(!useAI)}
                        className={`w-10 h-5 rounded-full relative transition-colors duration-300 ${useAI ? 'bg-purple-400' : 'bg-slate-400'}`}
                    >
                        <div className={`w-3.5 h-3.5 bg-white rounded-full absolute top-0.5 transition-all duration-300 ${useAI ? 'left-[22px]' : 'left-0.5'}`} />
                    </button>
                    <span className={`text-xs font-bold flex items-center gap-1 ${useAI ? 'text-white' : 'text-blue-300'}`}>
                        🤖 AI
                    </span>
                </div>
            </div>

            <form onSubmit={handleSubmit} className="p-6 space-y-6">
                {error && (
                    <div className="p-4 bg-red-50 text-red-700 rounded-lg flex items-center gap-2">
                        <AlertCircle className="w-5 h-5" /> {error}
                    </div>
                )}

                {/* Demographics */}
                <div className="grid grid-cols-2 gap-4">
                    <div>
                        <label className="block text-sm font-medium text-slate-700 mb-1">Age / العمر</label>
                        <input required type="number" value={formData.age} onChange={e => setFormData({ ...formData, age: e.target.value })} className="w-full rounded-md border-slate-300 shadow-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 py-2 px-3 border" placeholder="Years" />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-slate-700 mb-1">Gender / الجنس</label>
                        <select value={formData.gender} onChange={e => setFormData({ ...formData, gender: e.target.value })} className="w-full rounded-md border-slate-300 shadow-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 py-2 px-3 border">
                            <option value="male">Male / ذكر</option>
                            <option value="female">Female / أنثى</option>
                        </select>
                    </div>
                </div>

                {/* Complaint */}
                <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1 flex justify-between">
                        <span>Chief Complaint / الشكوى الرئيسية</span>
                        <span className="text-xs text-blue-600 font-normal flex items-center cursor-pointer hover:underline"><Mic className="w-3 h-3 mr-1" /> Voice Input (Soon)</span>
                    </label>
                    <textarea
                        required
                        value={formData.chief_complaint_text}
                        onChange={e => setFormData({ ...formData, chief_complaint_text: e.target.value })}
                        className="w-full rounded-md border-slate-300 shadow-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 py-2 px-3 border min-h-[100px]"
                        placeholder="Describe symptoms here... (e.g. 'Severe chest pain radiating to left arm' or 'عندي ألم في صدري')"
                        dir="auto"
                    />
                </div>

                {/* Vitals */}
                <div className="space-y-4 border-t pt-4">
                    <h3 className="text-sm font-semibold text-slate-900 flex items-center gap-2">
                        <Activity className="w-4 h-4 text-blue-600" /> Vital Signs / العلامات الحيوية
                    </h3>
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                        <div>
                            <label className="block text-xs text-slate-500">HR (bpm)</label>
                            <input type="number" name="hr" value={formData.vitals.hr} onChange={handleVitalChange} className="w-full rounded border-slate-300 border py-1.5 px-2 text-sm" placeholder="--" />
                        </div>
                        <div>
                            <label className="block text-xs text-slate-500">RR (bpm)</label>
                            <input type="number" name="rr" value={formData.vitals.rr} onChange={handleVitalChange} className="w-full rounded border-slate-300 border py-1.5 px-2 text-sm" placeholder="--" />
                        </div>
                        <div>
                            <label className="block text-xs text-slate-500">SpO2 (%)</label>
                            <input type="number" name="spo2" value={formData.vitals.spo2} onChange={handleVitalChange} className="w-full rounded border-slate-300 border py-1.5 px-2 text-sm" placeholder="--" />
                        </div>
                        <div>
                            <label className="block text-xs text-slate-500">Temp (°C)</label>
                            <input type="number" name="temp" value={formData.vitals.temp} onChange={handleVitalChange} className="w-full rounded border-slate-300 border py-1.5 px-2 text-sm" placeholder="--" />
                        </div>
                        <div>
                            <label className="block text-xs text-slate-500">SBP (mmHg)</label>
                            <input type="number" name="sbp" value={formData.vitals.sbp} onChange={handleVitalChange} className="w-full rounded border-slate-300 border py-1.5 px-2 text-sm" placeholder="--" />
                        </div>
                        <div>
                            <label className="block text-xs text-slate-500">DBP (mmHg)</label>
                            <input type="number" name="dbp" value={formData.vitals.dbp} onChange={handleVitalChange} className="w-full rounded border-slate-300 border py-1.5 px-2 text-sm" placeholder="--" />
                        </div>
                        <div>
                            <label className="block text-xs text-slate-500">GCS (3-15)</label>
                            <input type="number" name="gcs" value={formData.vitals.gcs} onChange={handleVitalChange} className="w-full rounded border-slate-300 border py-1.5 px-2 text-sm" max="15" min="3" />
                        </div>
                        <div>
                            <label className="block text-xs text-slate-500">Pain (0-10)</label>
                            <input type="number" name="pain_score" value={formData.vitals.pain_score} onChange={handleVitalChange} className="w-full rounded border-slate-300 border py-1.5 px-2 text-sm" max="10" min="0" />
                        </div>
                    </div>
                </div>

                <button
                    type="submit"
                    disabled={loading}
                    className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-lg shadow-sm transition-colors flex items-center justify-center gap-2 disabled:opacity-70"
                >
                    {loading ? 'Processing...' : 'Run Triage Assessment / تقييم'}
                    {!loading && <ChevronRight className="w-5 h-5" />}
                </button>
            </form>
        </div>
    );
}
