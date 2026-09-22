import { View, Text, ScrollView } from 'react-native';
import { useTrafficStore } from '../../store/trafficStore';

export default function DecisionsScreen() {
  const { decisions } = useTrafficStore();

  return (
    <ScrollView className="flex-1 bg-slate-900 p-4">
      <Text className="text-2xl font-bold text-white mb-4">AI Decision Timeline</Text>
      
      {decisions.length === 0 ? (
        <Text className="text-slate-400 text-center mt-10">No decisions recorded yet.</Text>
      ) : (
        decisions.map((decision, index) => (
          <View key={index} className="bg-slate-800 p-4 rounded-xl mb-4 border border-slate-700">
            <View className="flex-row justify-between mb-2">
              <Text className="text-blue-400 font-bold">{decision.intersection}</Text>
              <Text className="text-slate-400 text-xs text-right w-1/2" numberOfLines={1}>{new Date().toLocaleTimeString()}</Text>
            </View>
            <View className="flex-row items-center mb-2">
              <View className="bg-slate-700 px-3 py-1 rounded">
                <Text className="text-white font-bold">{decision.selected_phase}</Text>
              </View>
              <Text className="text-slate-300 ml-3">{decision.duration}s</Text>
            </View>
            <View className="mt-2 pt-2 border-t border-slate-700">
              <Text className="text-slate-400 text-xs uppercase mb-1">Reason:</Text>
              {decision.reason.map((r: string, i: number) => (
                <Text key={i} className="text-slate-200">• {r}</Text>
              ))}
            </View>
          </View>
        ))
      )}
    </ScrollView>
  );
}
