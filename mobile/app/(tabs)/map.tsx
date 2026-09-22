import { View, Text, StyleSheet } from 'react-native';
import { useTrafficStore } from '../../store/trafficStore';
import MapView, { Marker, Polyline } from 'react-native-maps';

export default function MapScreen() {
  const { intersections, roads, connected } = useTrafficStore();

  // Basic coordinates for our 4 intersections in a grid
  const coords: any = {
    "J1": { latitude: 13.0827, longitude: 80.2707 },
    "J2": { latitude: 13.0850, longitude: 80.2707 },
    "J3": { latitude: 13.0827, longitude: 80.2740 },
    "J4": { latitude: 13.0800, longitude: 80.2707 },
    "HOSPITAL": { latitude: 13.0827, longitude: 80.2780 },
  };

  if (!connected || intersections.length === 0) {
    return (
      <View className="flex-1 bg-slate-900 items-center justify-center">
        <Text className="text-white text-lg">Waiting for VAZHI-AI Data...</Text>
      </View>
    );
  }

  return (
    <View className="flex-1 bg-slate-900">
      <MapView
        style={StyleSheet.absoluteFillObject}
        initialRegion={{
          latitude: 13.0827,
          longitude: 80.2707,
          latitudeDelta: 0.01,
          longitudeDelta: 0.01,
        }}
        userInterfaceStyle="dark"
      >
        {/* Render Roads as Polylines */}
        {roads.map((road, idx) => {
          if (coords[road.source] && coords[road.target]) {
            const isCongested = road.occupancy > 0.8;
            return (
              <Polyline
                key={idx}
                coordinates={[coords[road.source], coords[road.target]]}
                strokeColor={isCongested ? "rgba(239, 68, 68, 0.8)" : "rgba(59, 130, 246, 0.5)"}
                strokeWidth={isCongested ? 6 : 4}
              />
            );
          }
          return null;
        })}

        {/* Render Intersections as Markers */}
        {intersections.map((intersection, idx) => {
          if (coords[intersection.id]) {
            return (
              <Marker
                key={idx}
                coordinate={coords[intersection.id]}
                title={intersection.name}
                description={`Phase: ${intersection.current_phase}`}
              >
                <View className={`p-2 rounded-full border-2 ${intersection.emergency ? 'bg-red-500 border-white' : 'bg-slate-800 border-blue-400'}`}>
                  <Text className="text-white font-bold text-xs">{intersection.id}</Text>
                </View>
              </Marker>
            );
          }
          return null;
        })}
        
        {/* Hospital Marker */}
        <Marker coordinate={coords["HOSPITAL"]} title="Hospital">
          <View className="p-2 bg-white rounded-full border-2 border-red-500">
            <Text className="text-red-500 font-bold text-xs">🏥</Text>
          </View>
        </Marker>
      </MapView>
      
      {/* Overlay Status */}
      <View className="absolute top-4 left-4 bg-slate-900/80 p-3 rounded-lg border border-slate-700">
        <Text className="text-white font-bold">LIVE MAP</Text>
        <Text className="text-slate-400 text-xs mt-1">
          {intersections.some(i => i.emergency) ? '🚨 EMERGENCY ACTIVE' : '🚦 NORMAL TRAFFIC'}
        </Text>
      </View>
    </View>
  );
}
