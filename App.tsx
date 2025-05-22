import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, SafeAreaView } from 'react-native';
import { Game } from './src/components/Game';

type Screen = 'MENU' | 'GAME' | 'OPTIONS';

export default function App() {
  const [screen, setScreen] = useState<Screen>('MENU');
  const [gameVariant, setGameVariant] = useState<'CLASSIC' | 'FRONTON'>('CLASSIC');

  const renderMenu = () => (
    <View style={styles.menuContainer}>
      <Text style={styles.title}>dRuBbLe</Text>
      <TouchableOpacity 
        style={styles.button} 
        onPress={() => setScreen('GAME')}
      >
        <Text style={styles.buttonText}>Play Classic</Text>
      </TouchableOpacity>
      <TouchableOpacity 
        style={styles.button} 
        onPress={() => {
          setGameVariant('FRONTON');
          setScreen('GAME');
        }}
      >
        <Text style={styles.buttonText}>Play Fronton</Text>
      </TouchableOpacity>
      <TouchableOpacity 
        style={styles.button} 
        onPress={() => setScreen('OPTIONS')}
      >
        <Text style={styles.buttonText}>Options</Text>
      </TouchableOpacity>
    </View>
  );

  const renderOptions = () => (
    <View style={styles.menuContainer}>
      <Text style={styles.title}>Options</Text>
      <TouchableOpacity 
        style={styles.button} 
        onPress={() => setScreen('MENU')}
      >
        <Text style={styles.buttonText}>Back to Menu</Text>
      </TouchableOpacity>
    </View>
  );

  return (
    <SafeAreaView style={styles.container}>
      {screen === 'MENU' && renderMenu()}
      {screen === 'OPTIONS' && renderOptions()}
      {screen === 'GAME' && <Game />}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  menuContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  title: {
    fontSize: 48,
    fontWeight: 'bold',
    marginBottom: 40,
    color: '#333',
  },
  button: {
    backgroundColor: '#4a90e2',
    paddingHorizontal: 30,
    paddingVertical: 15,
    borderRadius: 8,
    marginVertical: 10,
    minWidth: 200,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
}); 