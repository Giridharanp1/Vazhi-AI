import { create } from 'zustand';

interface TrafficState {
  time: number;
  running: boolean;
  intersections: any[];
  roads: any[];
  metrics: any;
  decisions: any[];
  connected: boolean;
  lastUpdated: number;
  updateState: (data: any) => void;
  setConnected: (status: boolean) => void;
}

export const useTrafficStore = create<TrafficState>((set) => ({
  time: 0,
  running: false,
  intersections: [],
  roads: [],
  metrics: {},
  decisions: [],
  connected: false,
  lastUpdated: 0,
  updateState: (data) => set((state) => ({
    ...data,
    decisions: data.decisions ? [...data.decisions, ...state.decisions].slice(0, 50) : state.decisions,
    lastUpdated: Date.now()
  })),
  setConnected: (status) => set({ connected: status })
}));
