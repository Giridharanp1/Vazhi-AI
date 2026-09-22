import { View, Text, ScrollView, TouchableOpacity, Alert } from 'react-native';
import { useTrafficStore } from '../../store/trafficStore';

export default function EmergencyScreen() {
  const { intersections, connected } = useTrafficStore();

  const triggerEmergency = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/events/ambulance', {
        method: 'POST',
      });
      if (res.ok) {
        Alert.alert('Emergency Scenario Started', 'Ambulance injected into the network.');
      }
    } catch (e) {
      Alert.alert('Error', 'Failed to connect to backend.');
    }
  };

  const hasEmergency = intersections.some(i => i.emergency);

  return (
    <ScrollView className="flex-1 bg-slate-900 p-4">
      <View className="mb-6 bg-slate-800 p-6 rounded-xl items-center border border-slate-700">
        <Text className="text-white text-xl font-bold mb-4">Demo Controls</Text>
        <TouchableOpacity 
          className="bg-red-600 px-8 py-4 rounded-full shadow-lg shadow-red-500/50"
          onPress={triggerEmergency}
          disabled={!connected}
        >
          <Text className="text-white font-bold text-lg">🚨 RUN EMERGENCY SCENARIO</Text>
        </TouchableOpacity>
        {!connected && <Text className="text-red-400 mt-2">Connect to backend first</Text>}
      </View>

      <Text className="text-2xl font-bold text-white mb-4">Emergency Corridors</Text>

      {hasEmergency ? (
        <View className="bg-red-900/50 p-4 rounded-xl border border-red-500 mb-4">
          <Text className="text-white font-bold text-lg mb-2">🚨 EMERGENCY CORRIDOR ACTIVE</Text>
          <Text className="text-slate-200 mb-4">Route: EXTERNAL → J2 → J1 → J3 → HOSPITAL</Text>
          
          {intersections.map(j => (
            j.id !== 'J4' && (
              <View key={j.id} className="flex-row justify-between items-center mb-2 bg-slate-800/50 p-3 rounded">
                <Text className="text-white font-bold">{j.name}</Text>
                {j.current_phase === 'EMERGENCY_CORRIDOR' ? (
                  <Text className="text-green-400 font-bold">READY ✓</Text>
                ) : (
                  <Text className="text-yellow-400 font-bold">PREPARING...</Text>
                )}
              </View>
            )
          ))}
          
        </View>
      ) : (
        <View className="items-center justify-center py-10">
          <Text className="text-slate-500 text-lg">No active emergencies in the network.</Text>
        </View>
      )}
    </ScrollView>
  );
}
