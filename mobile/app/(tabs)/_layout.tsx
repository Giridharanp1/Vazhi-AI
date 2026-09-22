import { SymbolView } from 'expo-symbols';
import { Tabs } from 'expo-router';
import Colors from '@/constants/Colors';
import { useColorScheme } from '@/components/useColorScheme';
import { useClientOnlyValue } from '@/components/useClientOnlyValue';

export default function TabLayout() {
  const colorScheme = useColorScheme();

  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: Colors[colorScheme ?? 'light'].tint,
        headerShown: useClientOnlyValue(false, true),
        tabBarStyle: {
          backgroundColor: colorScheme === 'dark' ? '#1E293B' : '#ffffff',
          borderTopColor: colorScheme === 'dark' ? '#334155' : '#e2e8f0',
        },
        headerStyle: {
          backgroundColor: colorScheme === 'dark' ? '#1E293B' : '#ffffff',
        },
        headerTintColor: colorScheme === 'dark' ? '#ffffff' : '#000000',
      }}>
      <Tabs.Screen
        name="index"
        options={{
          title: 'Home',
          tabBarIcon: ({ color }) => <SymbolView name={{ ios: 'house', android: 'home', web: 'house' }} tintColor={color} size={28} />,
        }}
      />
      <Tabs.Screen
        name="map"
        options={{
          title: 'Live Map',
          tabBarIcon: ({ color }) => <SymbolView name={{ ios: 'map', android: 'map', web: 'map' }} tintColor={color} size={28} />,
        }}
      />
      <Tabs.Screen
        name="emergency"
        options={{
          title: 'Emergency',
          tabBarIcon: ({ color }) => <SymbolView name={{ ios: 'staroflife', android: 'warning', web: 'staroflife' }} tintColor={color} size={28} />,
        }}
      />
      <Tabs.Screen
        name="decisions"
        options={{
          title: 'Decisions',
          tabBarIcon: ({ color }) => <SymbolView name={{ ios: 'list.bullet', android: 'list', web: 'list' }} tintColor={color} size={28} />,
        }}
      />
      <Tabs.Screen
        name="analytics"
        options={{
          title: 'Analytics',
          tabBarIcon: ({ color }) => <SymbolView name={{ ios: 'chart.bar', android: 'bar_chart', web: 'chart' }} tintColor={color} size={28} />,
        }}
      />
    </Tabs>
  );
}
