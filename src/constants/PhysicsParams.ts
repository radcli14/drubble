export const PhysicsParams = {
  // Physics constants
  g: 9.81,            // Gravitational acceleration [m/s^2]
  COR_s: [0.70, 0.90], // Coefficient of restitution when ball hits stool
  COR_g: [0.50, 0.70], // COR when ball hits ground
  COR_w: [0.80, 0.90], // COR when ball hits wall (for Fronton mode)
  rb: 0.2,            // Radius of the ball

  // Player parameters
  mc: 50.0,    // Mass of player [kg]
  mg: 2.0,     // Mass of stool [kg]
  m: 52.0,     // Total mass [kg]
  x0: 5.0,     // Initial player position [m]
  y0: 1.5,     // Equilibrium position of player CG [m]
  d: 0.3,      // Relative position from player CG to stool rotation axis [m]
  l0: 1.5,     // Equilibrium position of stool
  ax: 1.5,     // Horizontal acceleration [g]
  fy: 0.8,     // vertical frequency [Hz]
  fl: 2.2,     // Stool extension frequency
  ft: 1.25,    // Stool tilt frequency [Hz]
  vx: 10.0,    // Horizontal top speed [m/s]

  // Stool parameters
  stoolRadius: 0.35,
  stoolHandPos: -0.6,

  // Game settings
  frameRate: 60,
  dt: 1/60,
  dybtol: 4.0,        // Tolerance on last bounce speed before stopping motion
  
  // Fronton wall parameters
  wallDistance: 15.0,  // Distance to the wall from origin [m]
  wallHeight: 10.0,    // Height of the wall [m]
  wallWidth: 8.0,      // Width of the wall [m]
} as const;

// Derived parameters that depend on the above constants
export const DerivedParams = {
  Qx: PhysicsParams.ax * PhysicsParams.m * PhysicsParams.g,  // Max horizontal force [N]
  Ky: PhysicsParams.m * (PhysicsParams.fy * 2 * Math.PI) ** 2,  // Leg stiffness [N/m]
  Kl: PhysicsParams.mg * (PhysicsParams.fl * 2 * Math.PI) ** 2,  // Arm stiffness [N/m]
  Kt: (PhysicsParams.mg * PhysicsParams.l0 * PhysicsParams.l0) * (PhysicsParams.ft * 2 * Math.PI) ** 2,  // Tilt stiffness [N-m/rad]
} as const; 