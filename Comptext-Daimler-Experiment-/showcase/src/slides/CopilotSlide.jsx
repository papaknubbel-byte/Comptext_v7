import React from 'react';
import { motion } from 'framer-motion';

export default function CopilotSlide() {
  const anchors = ["PatternMatch: Critical", "KVTC_Frame_Integrity: 100%", "Semantic_Consistency: High"];
  const telemetryStatus = "Active (Tinybird)";

  return (
    <div className="flex flex-col items-center justify-center h-full p-12 text-white">
      <motion.h1 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-4xl font-bold mb-8 text-[#00A0DC]"
      >
        Enterprise AI / Copilot Preview
      </motion.h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 w-full max-w-4xl">
        {/* Interpretability Block */}
        <motion.div 
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-[#1A2233] p-6 rounded-xl border border-[#2A354C]"
        >
          <h2 className="text-xl font-semibold mb-4 text-[#0DCFFF]">Interpretability Layer</h2>
          <div className="space-y-4">
            <div>
              <p className="text-sm text-[#8899AA]">Confidence Score</p>
              <div className="flex items-center gap-3">
                <div className="h-2 flex-1 bg-[#0D1117] rounded-full overflow-hidden">
                  <motion.div 
                    initial={{ width: 0 }}
                    animate={{ width: "95%" }}
                    transition={{ duration: 1, delay: 0.5 }}
                    className="h-full bg-green-500"
                  />
                </div>
                <span className="text-xs font-mono">0.95</span>
              </div>
            </div>
            <div>
              <p className="text-sm text-[#8899AA]">Thought Anchors</p>
              <div className="flex flex-wrap gap-2 mt-2">
                {anchors.map((a, i) => (
                  <span key={i} className="text-[10px] bg-[#0D1117] px-2 py-1 rounded border border-[#2A354C] text-[#0DCFFF]">
                    {a}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </motion.div>

        {/* Sync & Telemetry Block */}
        <motion.div 
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-[#1A2233] p-6 rounded-xl border border-[#2A354C]"
        >
          <h2 className="text-xl font-semibold mb-4 text-[#0DCFFF]">Enterprise Connectivity</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-[#8899AA]">Copilot Sync Status</span>
              <span className="flex items-center gap-2 text-green-500 text-xs">
                <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                Synchronized
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-[#8899AA]">MS Graph Connector</span>
              <span className="text-xs text-[#8899AA] font-mono italic">Simulation Mode</span>
            </div>
            <div className="pt-4 border-t border-[#2A354C]">
              <p className="text-xs text-[#8899AA] mb-2 uppercase tracking-widest">Telemetry Node</p>
              <p className="text-sm font-mono text-[#0DCFFF]">{telemetryStatus}</p>
            </div>
          </div>
        </motion.div>
      </div>

      <motion.p 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.8 }}
        className="mt-12 text-sm text-[#556677] italic"
      >
        "Bridging deep industrial compression with high-level enterprise visibility."
      </motion.p>
    </div>
  );
}
