import { motion } from 'framer-motion';

const FEATURES = [
  { 
    id: 'L12_N452', 
    label: 'Brake Integrity', 
    activation: 0.9842, 
    explanation: 'Responds to mentions of critical vehicle safety systems and braking anomalies.' 
  },
  { 
    id: 'L08_N122', 
    label: 'CAN-Bus Sync', 
    activation: 0.8215, 
    explanation: 'Activates on sequences containing diagnostic trouble codes related to CAN-bus timeouts.' 
  },
  { 
    id: 'L15_N891', 
    label: 'Thermal Stress', 
    activation: 0.7561, 
    explanation: 'Responds to high-density numeric data within KVTC frames indicating thermal stress.' 
  },
];

export default function InterpretabilitySlide() {
  return (
    <div className="w-full h-full flex flex-col justify-center px-12 py-10 max-w-6xl mx-auto">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <div className="text-xs font-mono tracking-widest text-[#00C853] uppercase mb-2">07 / Interpretability</div>
        <h2 className="text-4xl font-black">
          NLA <span className="text-gradient" style={{ background: 'linear-gradient(135deg, #00C853 0%, #69F0AE 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>Explainability</span>
        </h2>
        <p className="text-[#8899AA] mt-1 max-w-2xl">
          Unsupervised explanations of LLM activations using Natural Language Autoencoders. 
          Deconstructing the industrial "Black Box".
        </p>
      </motion.div>

      <div className="grid grid-cols-1 gap-4 max-w-4xl">
        {FEATURES.map((f, i) => (
          <motion.div
            key={f.id}
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.1 }}
            className="card p-5 flex items-center gap-6 relative overflow-hidden group hover:border-[#00C853] transition-colors"
            style={{ borderColor: 'rgba(0, 200, 83, 0.2)', background: 'rgba(10, 31, 16, 0.3)' }}
          >
             {/* Activation Progress Bar Background */}
             <motion.div 
              initial={{ width: 0 }}
              animate={{ width: `${f.activation * 100}%` }}
              transition={{ duration: 1.5, delay: 0.5 + i * 0.1 }}
              className="absolute inset-0 bg-[#00C85308] pointer-events-none"
            />

            <div className="flex-shrink-0 w-16 h-16 rounded-full border-2 border-[#00C85333] flex items-center justify-center relative bg-[#0D1526]">
                <svg className="absolute inset-0 w-full h-full -rotate-90">
                    <circle 
                        cx="32" cy="32" r="28" 
                        fill="transparent" 
                        stroke="rgba(0,200,83,0.1)" 
                        strokeWidth="4" 
                    />
                    <motion.circle 
                        cx="32" cy="32" r="28" 
                        fill="transparent" 
                        stroke="#00C853" 
                        strokeWidth="4" 
                        strokeDasharray="176"
                        initial={{ strokeDashoffset: 176 }}
                        animate={{ strokeDashoffset: 176 - (176 * f.activation) }}
                        transition={{ duration: 1.5, delay: 0.5 + i * 0.1 }}
                    />
                </svg>
                <span className="text-xs font-mono font-bold text-[#00C853]">{Math.round(f.activation * 100)}%</span>
            </div>

            <div className="flex-1 z-10">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-[10px] font-mono text-[#00C853] uppercase tracking-tighter">{f.id}</span>
                <span className="text-[9px] bg-[#00C85322] text-[#00C853] px-1.5 py-0.5 rounded-sm border border-[#00C85333]">UNSUPERVISED</span>
                <h3 className="text-base font-bold text-white ml-2">{f.label}</h3>
              </div>
              <p className="text-sm text-[#8899AA] font-medium italic">
                "{f.explanation}"
              </p>
            </div>

            <div className="hidden md:flex flex-col items-end gap-1 z-10">
              <div className="text-[9px] text-[#445566] uppercase font-mono">Activation Trace</div>
              <div className="flex items-end gap-0.5 h-6">
                {[...Array(15)].map((_, j) => (
                  <motion.div 
                    key={j} 
                    initial={{ height: 0 }}
                    animate={{ height: `${20 + Math.random() * 80}%` }}
                    transition={{ repeat: Infinity, duration: 0.5 + Math.random(), repeatType: 'reverse' }}
                    className="w-0.5 bg-[#00C853]" 
                    style={{ opacity: 0.3 + (Math.random() * 0.4) }} 
                  />
                ))}
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.0 }}
        className="mt-8 p-4 rounded-xl bg-[#00C8530a] border border-[#00C85322] flex items-center gap-4 max-w-4xl"
      >
        <span className="text-2xl">🔬</span>
        <p className="text-xs text-[#8899AA] leading-relaxed font-mono">
          <strong className="text-[#00C853]">Research Insight:</strong> CompText V6 implements the <em className="text-white">Natural Language Autoencoders</em> methodology. 
          By mapping sparse autoencoder features to natural language, we achieve a deterministic audit trail for LLM-based industrial decisions.
        </p>
      </motion.div>
    </div>
  );
}
