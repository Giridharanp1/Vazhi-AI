import { View, Text, StyleSheet } from 'react-native';
import { useTrafficStore } from '../../store/trafficStore';

export default function MapScreenWeb() {
  const { intersections, roads, connected } = useTrafficStore();

  if (!connected || intersections.length === 0) {
    return (
      <View className="flex-1 bg-slate-900 items-center justify-center">
        <Text className="text-white text-lg">Waiting for VAZHI-AI Data...</Text>
      </View>
    );
  }

  return (
    <View className="flex-1 bg-slate-900 justify-center items-center p-4">
      <View className="absolute top-4 left-4 bg-slate-900/80 p-3 rounded-lg border border-slate-700 z-10">
        <Text className="text-white font-bold">LIVE MAP (WEB VIEW)</Text>
        <Text className="text-slate-400 text-xs mt-1">
          {intersections.some(i => i.emergency) ? '🚨 EMERGENCY ACTIVE' : '🚦 NORMAL TRAFFIC'}
        </Text>
      </View>

      <Text className="text-white text-lg mb-4 text-center">
        Note: The interactive Map is optimized for the mobile app (iOS/Android) using react-native-maps. 
        Below is a simplified web representation of the network state.
      </Text>

      <View className="flex-row flex-wrap justify-center max-w-2xl">
        {intersections.map(j => {
          const isEmergency = j.emergency;
          return (
            <View key={j.id} className={`m-4 p-6 rounded-full border-4 items-center justify-center w-32 h-32 ${isEmergency ? 'bg-red-900 border-red-500' : 'bg-slate-800 border-blue-500'}`}>
              <Text className="text-white font-bold text-xl">{j.id}</Text>
              <Text className="text-slate-300 text-xs mt-1">{j.current_phase}</Text>
              {isEmergency && <Text className="text-red-300 mt-1 font-bold">🚨</Text>}
            </View>
          );
        })}
      </View>

    </View>
  );
}
