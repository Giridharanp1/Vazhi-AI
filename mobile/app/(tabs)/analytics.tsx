import { View, Text, ScrollView } from 'react-native';
import { useTrafficStore } from '../../store/trafficStore';

export default function AnalyticsScreen() {
  const { metrics } = useTrafficStore();

  return (
    <ScrollView className="flex-1 bg-slate-900 p-4">
      <Text className="text-2xl font-bold text-white mb-6">Simulation Metrics</Text>
      
      <View className="flex-row flex-wrap justify-between">
        
        <View className="bg-slate-800 p-4 rounded-xl w-[48%] mb-4 border border-slate-700">
          <Text className="text-slate-400 mb-1 text-xs uppercase">Avg Waiting Time</Text>
          <Text className="text-3xl font-bold text-blue-400">
            {metrics.avg_wait?.toFixed(1) || 0}s
          </Text>
        </View>

        <View className="bg-slate-800 p-4 rounded-xl w-[48%] mb-4 border border-slate-700">
          <Text className="text-slate-400 mb-1 text-xs uppercase">Max Queue Length</Text>
          <Text className="text-3xl font-bold text-warning">
            {metrics.max_queue || 0}
          </Text>
        </View>

        <View className="bg-slate-800 p-4 rounded-xl w-[100%] mb-4 border border-slate-700">
          <Text className="text-slate-400 mb-1 text-xs uppercase">Network Throughput</Text>
          <Text className="text-3xl font-bold text-success">
            {metrics.throughput || 0} veh/min
          </Text>
        </View>

        <View className="bg-slate-800 p-4 rounded-xl w-[48%] mb-4 border border-slate-700">
          <Text className="text-slate-400 mb-1 text-xs uppercase">Spillback Events</Text>
          <Text className="text-3xl font-bold text-red-400">
            {metrics.spillback_events || 0}
          </Text>
        </View>

        <View className="bg-slate-800 p-4 rounded-xl w-[48%] mb-4 border border-slate-700">
          <Text className="text-slate-400 mb-1 text-xs uppercase">Signal Switches</Text>
          <Text className="text-3xl font-bold text-purple-400">
            {metrics.signal_switches || 0}
          </Text>
        </View>
        
      </View>
      
      <View className="mt-8 bg-blue-900/30 p-4 rounded-xl border border-blue-500/50">
        <Text className="text-blue-300 font-bold mb-2">VAZHI-AI vs Fixed-Time</Text>
        <Text className="text-slate-300 text-sm">
          VAZHI-AI dynamically adjusts to traffic states. In a fixed-time scenario, 
          the average waiting time would scale linearly with downstream congestion. 
          Currently simulating adaptive control.
        </Text>
      </View>

    </ScrollView>
  );
}
