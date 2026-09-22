import { View, Text, ScrollView, TouchableOpacity } from 'react-native';
import { useTrafficStore } from '../../store/trafficStore';
import { useRouter } from 'expo-router';

export default function HomeScreen() {
  const { connected, metrics, intersections, time } = useTrafficStore();
  const router = useRouter();

  const activeEmergencies = intersections.filter(i => i.emergency).length;
  const congestedJunctions = intersections.filter(i => 
    Object.values(i.downstream).some((occ: any) => occ > 0.8)
  ).length;

  return (
    <ScrollView className="flex-1 bg-slate-900 p-4">
      <View className="mb-6">
        <Text className="text-3xl font-bold text-white mb-2">VAZHI-AI</Text>
        <View className="flex-row items-center">
          <View className={`w-3 h-3 rounded-full mr-2 ${connected ? 'bg-green-500' : 'bg-red-500'}`} />
          <Text className="text-slate-300">
            {connected ? 'LIVE STATUS' : 'CONNECTION LOST'}
          </Text>
        </View>
        <Text className="text-slate-400 mt-1">Simulation Time: {time}s</Text>
      </View>

      <View className="flex-row flex-wrap justify-between mb-6">
        <View className="bg-slate-800 p-4 rounded-xl w-[48%] mb-4">
          <Text className="text-slate-400 mb-1">Active Emergencies</Text>
          <Text className="text-2xl font-bold text-red-500">{activeEmergencies}</Text>
        </View>
        <View className="bg-slate-800 p-4 rounded-xl w-[48%] mb-4">
          <Text className="text-slate-400 mb-1">Congested Junctions</Text>
          <Text className="text-2xl font-bold text-warning">{congestedJunctions}</Text>
        </View>
        <View className="bg-slate-800 p-4 rounded-xl w-[100%]">
          <Text className="text-slate-400 mb-1">Network Avg Waiting Time</Text>
          <Text className="text-3xl font-bold text-blue-400">{metrics.avg_wait?.toFixed(1) || 0}s</Text>
        </View>
      </View>

      <TouchableOpacity 
        className="bg-blue-600 p-4 rounded-xl items-center"
        onPress={() => router.push('/map')}
      >
        <Text className="text-white font-bold text-lg">VIEW LIVE MAP</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}
