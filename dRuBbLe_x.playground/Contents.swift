import UIKit

// Timing variables
let fs = 60.0
let dt = 1/fs

// For keyboard input, set the state of the arrows and W-A-S-D
var keyPush = [0, 0, 0, 0, 0, 0, 0, 0]

// Color definition
let red       = (1.0, 0.0, 0.0)
let green     = (0.0, 1.0, 0.0)
let blue      = (0.0, 0.0, 1.0)
let darkBlue  = (0.0, 0.0, 128.0/255.0)
let white     = (1.0, 1.0, 1.0)
let gray      = (160.0/255.0, 160.0/255.0, 160.0/255.0)
let black     = (0.0, 0.0, 0.0)
let pink      = (1.0, 100.0/255.0, 100.0/255.0)
let skyBlue   = (135.0/255.0, 206.0/255.0, 235.0/255.0)
let darkGreen = (0.0, 120.0/255.0, 0)

// Create the value of pi
let pi = 3.14159

// Convert physical coordinates to pixels
func xy2p(x: Double, y: Double, m2p: Double,po: Double,w: Double,h: Double) -> (Double, Double) {
    let xout = x*m2p-po+w/2
    let yout = y*m2p+h/20
    return (xout, yout)
}

// Define the linspace function
func linspace(startValue: Double, endValue: Double, nSteps: Int) -> [Double] {
    var outputArray = [Double]()
    let incrementSize = (endValue - startValue) / Double(nSteps - 1)
    for n in 0 ..< nSteps {
        outputArray.append(startValue + Double(n) * incrementSize)
    }
    return outputArray
}

// Calculate the vector norm (length)
func norm(vec: [Double]) -> Double {
    var vec2 = 0.0
    for n in 0 ..< vec.count {
        vec2 += pow(vec[n], 2)
    }
    return sqrt(vec2)
}

// Solves for the location of the knee or elbow based upon the two other end-points of the triangle
func thirdPoint(P0: [Double], P1: [Double], L: Double, SGN: Int) -> [Double] {
    // Subtract then add the two points
    let Psub = [P0[0] - P1[0], P0[1] - P1[1]]
    let Padd = [P0[0] + P1[0], P0[1] + P1[1]]
    
    // Calculate the midpoint between the two
    let P2 = [Padd[0] / 2.0, Padd[1] / 2.0]
    
    // Distance between point P0, P1
    let d = norm(vec: Psub)
    
    var P3 = [0.0, 0.0]
    if d > L {
        // P0 and P1 are too far apart to form a knee, use the midpoint
        P3 = P2
    } else {
        let a = pow(d, 2) / 2.0 / d  // Distance to mid-Point
        let h = sqrt(pow(L, 2) / 4.0 - pow(a, 2))
        let x3 = P2[0] + h * Double(SGN) * Psub[1] / d
        let y3 = P2[1] - h * Double(SGN) * Psub[0] / d
        P3 = [x3, y3]
    }
    return P3
}

// Solve for the vertices that make up the stick man and stool
func stickDude(u: [Double], k: Int) -> ([Double], [Double], [Double], [Double]) {
    let k8 = k*8
    // Get the state variables
    // States from u
    let x = u[4+k8]
    let y = u[5+k8]
    let l = u[6+k8]
    let th = u[7+k8]
    let v = u[8+k8]
    
    let s = sin(th)
    let c = cos(th)
    
    // Right Foot [rf] Left Foot [lf] Positions
    let rf = [x - 0.25 + (v / p.vx) * sin(1.5 * x + 3.0 * pi / 2.0),
              0.2 * (v / p.vx) * (1 + sin(1.5 * x + 3.0 * pi / 2.0))]
    let lf = [x + 0.25 + (v / p.vx) * cos(1.5 * x),
              0.2 * (v / p.vx) * (1 + cos(1.5 * x))]
    
    // Waist Position
    let w = [x, y-p.d]
    
    // Right Knee [rk] Left Knee [lk] Positions
    let rk = thirdPoint(P0: w, P1: rf, L: p.y0-p.d, SGN: -1)
    let lk = thirdPoint(P0: w, P1: lf, L: p.y0-p.d, SGN: 1)
    
    // Shoulder Position
    let sh = [x, y+p.d]
    let shl = [x - 0.18, y + p.d + 0.05]
    let shr = [x + 0.18, y + p.d + 0.05]
    
    // Stool Position
    var sx = [Double]()
    var sy = [Double]()
    for n in 0 ..< 13 {
        sx.append(x + p.xs[n] * c - (l + p.ys[n]) * s)
        sy.append(y + p.d + (l + p.ys[n]) * c + p.xs[n] * s)
    }
    
    // Right Hand [rh] Left Hand [lh] Position
    let rh = [sx[7], sy[7]]
    let lh = [sx[6], sy[6]]
    
    // Right Elbow [re] Left Elbow [le] Position
    let re = thirdPoint(P0: shl, P1: rh, L: 1, SGN: 1)
    let le = thirdPoint(P0: shr, P1: lh, L: 1, SGN: -1)
    
    // Plotting vectors
    let xv = [rf[0], rk[0], w[0], lk[0], lf[0], lk[0], w[0], sh[0], shl[0], re[0], rh[0], re[0], shl[0],    shr[0], le[0], lh[0]]
    let yv = [rf[1], rk[1], w[1], lk[1], lf[1], lk[1], w[1], sh[1], shl[1], re[1], rh[1], re[1], shl[1], shr[1], le[1], lh[1]]
    
    return (xv, yv, sx, sy)
}

func ballHitStool(t: Double, u: [Double], k: Int) -> Double {
    // Unpack the state variables
    let xb = u[0]
    let yb = u[1]
    
    // Get the stool locations using stickDude function
    let (_, _, sx, sy) = stickDude(u: u, k: k)
    
    // Vectors from the left edge of the stool to the right, and to the ball
    let r1 = [sx[1] - sx[0], sy[1] - sy[0]]
    
    // Calculate z that minimizes the distance
    let z = ((xb - sx[0]) * r1[0] + (yb - sy[0]) * r1[1])/(pow(r1[0], 2) + pow(r1[1], 2))
    
    // Find the closest point of impact on the stool
    var ri = [0.0, 0.0]
    if z < 0 {
        ri = [sx[0], sy[0]]
    } else if z > 1 {
        ri =  [sx[1], sy[1]]
    } else {
        ri = [sx[0] + z * r1[0], sy[0] + z * r1[1]]
    }
    
    // Vector from the closest point of impact to the center of the ball
    let r2 = [xb - ri[0], yb - ri[1]]
    
    // Calculate the distance to the outer radius of the ball t
    let L = norm(vec: r2) - p.rb
    
    return L
}

func ballHitFloor(t: Double, u: [Double]) -> Double {
    return u[1] - p.rb
}


// Set up the parameter class, contains constants
class Parameters {
    // Game parameters
    let g = 9.81   // Gravitational acceleration [m/s^2]
    let COR = 0.8  // Coefficient of restitution
    let rb = 0.2   // Radius of the ball

    // Player parameters
    let mc = 50.0  // Mass of player [kg]
    let mg = 2.0   // Mass of stool [kg]
    let x0 = 5.0   // Initial player position [m]
    let y0 = 1.5   // Equilibrium position of player CG [m]
    let d = 0.3    // Relative position from player CG to stool rotation axis [m]
    let l0 = 1.5   // Equilibrium position of stool
    let ax = 1.0   // Horizontal acceleration [g]
    let Gx = 1.5   // Control gain on Qx
    let fy = 0.8   // vertical frequency [Hz]
    let fl = 2.2   // Stool extension frequency
    let ft = 1.5   // Stool tilt frequency [Hz]
    let Gt = 0.8   // Control gain on Qt
    let vx = 10.0  // Horizontal top speed [m/s]
    let zy = 0.1   // Vertical damping ratio
    let zl = 0.08  // Arm damping ratio
    let zt = 0.09  // Stool tilt damping ratio

    //Gameplay settings
    let userControlled = [[true,   true,  true,  true],
                          [false, false, false, false]]
    var nPlayer = 1

    // Stool parameters
    let xs = [-0.25,  0.25,  0.15,
              0.20, -0.20,  0.20,
              0.25, -0.25,  0.25,
              0.30,  0.25, -0.25, -0.30]
    let ys = [0.00,  0.00,  0.00,
              -0.30, -0.30, -0.30,
              -0.60, -0.60, -0.60,
              -0.90,  0.00,  0.00, -0.90]

    // Touch Stick Sensitivity
    let tsens = 1.5

    // Tolerance on last bounce speed before stopping motion
    let dybtol = 2.0

    // startAngle (sa) and startSpeed (ss) initially
    let sa = pi/4
    let ss = 10.0

    // Parameter settings I'm using to try to improve running speed
    let linearMass = false
    let nEulerSteps = 1

    // Font settings
    let MacsFavoriteFont = "Optima"

    // Color settings
    let playerColor = (darkGreen, red)
    let stoolColor = (white, black)
    
    // Initialize derived parameters
    var m = 0.0, Qx = 0.0, Ky = 0.0, Qy = 0.0, Kl = 0.0, Ql = 0.0, Kt = 0.0, Qt = 0.0, Cx = 0.0, Cy = 0.0, Cl = 0.0, Ct = 0.0
    var q0 = [Double]()
    var u0 = [Double]()
    init() {
        self.m = self.mc + self.mg                                   // Total mass [kg]
        self.Qx = self.ax * self.m * self.g                          // Max horizontal force [N]
        self.Ky = self.m * (self.fy * 2 * pi) * (self.fy * 2 * pi)   // Leg stiffness [N/m]
        self.Qy = self.Ky*0.3                                        // Leg strength [N], to be updated
        self.Kl = self.mg * (self.fl * 2 * pi) * (self.fl * 2 * pi)  // Arm stiffness [N/m]
        self.Ql = self.Kl*0.3                                        // Arm strength [N]
        self.Kt = (mg * l0 * l0) * (ft * 2 * pi) * (ft * 2 * pi)     // Tilt stiffness [N-m/rad]
        self.Qt = 0.6*self.Kt                                        // Tilt strength [N-m]
        self.Cx = self.Qx / self.vx                                  // Horizontal damping [N-s/m]
        self.Cy = 2 * self.zy * sqrt(self.Ky * self.m)               // Vertical damping [N-s/m]
        self.Cl = 2 * self.zl * sqrt(self.Kl * self.m)               // Arm damping [N-s/m]
        self.Ct = 2.0 * self.zl * sqrt(self.Kt * self.m)             // Tilt damping [N-m-s/rad]

        // Initial states
        self.q0 = [0.0, self.y0, self.l0, 0.0]
        self.u0 = [0.0, self.rb,     0.0, 0.0, self.x0, self.y0, self.l0,   0.0, 0.0, 0.0, 0.0, 10.0,
                   0.0, self.y0, self.l0, 0.0,     0.0,     0.0,     0.0, -10.0]

    }
}

var p = Parameters()
print(p.u0)


class GameScore {
    // Initiate statistics as zeros
    var t = 0.0
    var n = 0
    var stoolCount = 0
    var stoolDist = 0.0
    var maxHeight = 0.0
    var floorCount = 0
    var score = 0
    var averageStepTime = 0.0
    
    func update(t: Double, n: Int, xb: Double, yb: Double, StoolBounce: Bool, FloorBounce: Bool) {
        self.t = t
        self.n = n
        if StoolBounce && self.stoolDist < xb {
            self.stoolDist = xb
        }
        if self.maxHeight < yb && self.stoolCount > 0 {
            self.maxHeight = yb
        }
        self.stoolCount += StoolBounce ? 1 : 0
        self.floorCount += FloorBounce ? 1 : 0
        self.score = Int(self.stoolDist * self.maxHeight * Double(self.stoolCount))
    }
    
    func re_init() {
        // Re-initiate statistics as zeros
        self.t = 0.0
        self.n = 0
        self.stoolCount = 0
        self.stoolDist = 0.0
        self.maxHeight = 0.0
        self.floorCount = 0
        self.score = 0
        self.averageStepTime = 0.0
    }
}

var stats = GameScore()
print(stats.t)

class GameState {
    // Define Game Mode
    // 0 = Quit
    // 1 = Splash screen
    // 2 = Options screen
    // 3 = In game, pre-angle set
    // 4 = In game, angle set
    // 5 = In game, distance set
    // 6 = In game
    // 7 = Game over, resume option
    // 8 = Game over, high scores
    var game_mode = 1
    var showedSplash = false
    
    // Initialize the ctrl (control) array
    var ctrl = [0.0, 0.0, 0.0, 0.0]
    var ctrlMode = "Keys"
    var ctrlFunc = 0
    
    // Timing
    var t = 0.0, n = 0, te = 0.0
    
    // State variables
    var u = p.u0
    var xb: Double, yb: Double, dxb: Double, dyb: Double
    var xp: [Double], yp: [Double], lp: [Double], tp: [Double]
    var dxp: [Double], dyp: [Double], dlp: [Double], dtp: [Double]
    var xI: Double, yI: Double, tI: Double, xTraj = [Double](), yTraj = [Double](), timeUntilBounce: Double
    // TBR self.xI, self.yI, self.tI, self.xTraj, self.yTraj, self.timeUntilBounce = BallPredict(self)
    
    // Event states
    var ue: [Double]
    
    // Initial ball angle and speed conditions
    var startAngle: Double, startSpeed: Double, phase: Double
    
    // Stuck condition
    var Stuck = false
    
    // Initial assumption, there was no event
    var StoolBounce = false
    var FloorBounce = false
    
    // Init is called when the class is created
    init() {
        // Timing
        self.t = 0.0
        self.n = 0
        self.te = 0.0
        
        // State variables
        self.xb = p.u0[0]
        self.yb = p.u0[1]
        self.dxb = p.u0[2]
        self.dyb = p.u0[3]
        self.xp = [p.u0[4], p.u0[12]]
        self.yp = [p.u0[5], p.u0[13]]
        self.lp = [p.u0[6], p.u0[14]]
        self.tp = [p.u0[7], p.u0[15]]
        self.dxp = [p.u0[8], p.u0[16]]
        self.dyp = [p.u0[9], p.u0[17]]
        self.dlp = [p.u0[10], p.u0[18]]
        self.dtp = [p.u0[11], p.u0[19]]
        self.xI = 0.0
        self.yI = 0.0
        self.tI = 0.0
        self.xTraj = [0.0]
        self.yTraj = [0.0]
        self.timeUntilBounce = 0.0
        
        // Event states
        self.ue = p.u0
        
        // Initial ball angle and speed conditions
        self.startAngle = p.sa
        self.startSpeed = p.ss
        self.phase      = 0.0
        
        // Stuck condition
        self.Stuck = false
    }
    
    // re_init() is used to restart the game, its the same as init()
    func re_init() {
        // Timing
        self.t = 0.0
        self.n = 0
        self.te = 0.0
        
        // State variables
        self.xb = p.u0[0]
        self.yb = p.u0[1]
        self.dxb = p.u0[2]
        self.dyb = p.u0[3]
        self.xp = [p.u0[4], p.u0[12]]
        self.yp = [p.u0[5], p.u0[13]]
        self.lp = [p.u0[6], p.u0[14]]
        self.tp = [p.u0[7], p.u0[15]]
        self.dxp = [p.u0[8], p.u0[16]]
        self.dyp = [p.u0[9], p.u0[17]]
        self.dlp = [p.u0[10], p.u0[18]]
        self.dtp = [p.u0[11], p.u0[19]]
        self.xI = 0.0
        self.yI = 0.0
        self.tI = 0.0
        self.xTraj = [0.0]
        self.yTraj = [0.0]
        self.timeUntilBounce = 0.0
        
        // Event states
        self.ue = p.u0
        
        // Initial ball angle and speed conditions
        self.startAngle = p.sa
        self.startSpeed = p.ss
        self.phase      = 0.0
        
        // Stuck condition
        self.Stuck = false
    }
    
    
    // Rename the state variables
    func var_states() {
        self.xb = self.u[0]
        self.yb = self.u[1]
        self.dxb = self.u[2]
        self.dyb = self.u[3]
        self.xp = [self.u[4], self.u[12]]
        self.yp = [self.u[5], self.u[13]]
        self.lp = [self.u[6], self.u[14]]
        self.tp = [self.u[7], self.u[15]]
        self.dxp = [self.u[8], self.u[16]]
        self.dyp = [self.u[9], self.u[17]]
        self.dlp = [self.u[10], self.u[18]]
        self.dtp = [self.u[11], self.u[19]]
    }
    
    func cycle_modes() {
        if self.game_mode == 1 {
            // Exit splash screen
            self.game_mode += 1
        } else if gs.game_mode == 2 {
            // Exit options screen and reset game
            stats.re_init()
            self.re_init()
            self.game_mode = 3
        } else if (self.game_mode == 3 || self.game_mode == 4) {
            // Progress through angle and speed selection
            self.game_mode += 1
            self.phase = 0
        } else if self.game_mode == 5 {
            // Start the ball moving!
            self.game_mode = 6
        } else if self.game_mode == 6 {
            // Reset the game
            stats.re_init()
            self.re_init()
            self.game_mode = 3
        }
    }
    
    func setAngleSpeed() {
        if self.game_mode == 4 {
            self.startAngle = 0.25*pi*(1 + 0.75*sin(self.phase))
        } else if self.game_mode == 5 {
            self.startSpeed = p.ss*(1 + 0.75*sin(self.phase))
        }
        if self.game_mode == 4 || self.game_mode == 5 {
            self.phase += 3.0 * dt
            self.u[2] = self.startSpeed * cos(self.startAngle)
            self.u[3] = self.startSpeed * sin(self.startAngle)
        }
    }
    
    // Define a function to predict motion of the ball
    func ball_predict() {
        if self.dyb == 0 || self.game_mode <= 2 {
            // Ball is not moving, impact time is zero
            self.tI = 0
        } else if self.game_mode > 2 && (self.dyb > 0) && (self.yb < self.yp[0] + p.d + self.lp[0]) {
            // Ball is in play, moving upward and below the stool
            // Solve for time and height at apogee
            let ta = self.dyb / p.g
            let ya = 0.5 * p.g * pow(ta, 2)
        
            // Solve for time the ball would hit the ground
            self.tI = ta + sqrt(2.0 * ya / p.g)
        } else if self.game_mode > 2 || (self.yb > self.yp[0] + p.d + self.lp[0]) {
            // Ball is in play, above the stool
            // Solve for time that the ball would hit the stool
            self.tI = -(-self.dyb - sqrt(pow(self.dyb, 2) + 2.0 * p.g * (self.yb - self.yp[0] - p.d - self.lp[0]))) / p.g
        } else {
            self.tI = 0
        }
        
        if self.tI.isNaN {
            self.tI = 0
        }
        
        // Solve for position that the ball would hit the stool
        self.xI = self.xb + self.dxb * self.tI
        self.yI = self.yb + self.dyb * self.tI - 0.5 * p.g * pow(self.tI, 2)
        
        // Solve for time that the ball would hit the ground
        let tG = -(-self.dyb - sqrt(pow(self.dyb, 2) + 2.0 * p.g * self.yb)) / p.g
        
        // Solve for the arc for the next 1.2 seconds, or until ball hits ground
        let T = linspace(startValue: 0.0, endValue: min(1.2, tG), nSteps: 20)
        self.xTraj = [Double]()
        self.yTraj = [Double]()
        for n in 0 ..< 20 {
            self.xTraj.append(self.xb + self.dxb * T[n])
            self.yTraj.append(self.yb + self.dyb * T[n] - 0.5 * p.g * pow(T[n], 2))
        }
        
        // Time until event
        self.timeUntilBounce = tI
        self.tI = self.timeUntilBounce + self.t
        
    }
    
    // Get control input from external source
    func set_control(keyPush: [Int] = [0, 0, 0, 0, 0, 0, 0, 0], moveStick: [Double] = [0, 0], tiltStick: [Double] = [0, 0], g: [Double] = [0, 0, 0], a: [Double] = [0, 0, 0]) {

        if self.ctrlFunc == 0 {
            // Key press control
            self.ctrl = [Double(keyPush[1]-keyPush[0]), Double(keyPush[2]-keyPush[3]), Double(keyPush[4]-keyPush[5]), Double(keyPush[6]-keyPush[7])]
        } else if self.ctrlFunc == 1 {
            // Motion control scale factors
            let gThreshold = 0.05
            let slope = 5.0
            let aScale = 2.0
            
            // Run left/right
            if g[1] > gThreshold {
                self.ctrl[0] = -min(slope*(g[1]-gThreshold), 1)
            } else if g[1] < -gThreshold {
                self.ctrl[0] = -max(slope*(g[1]+gThreshold), -1)
            } else {
                self.ctrl[0] = 0.0
            }
            
            // Push up/down
            if a[1] > 0 {
                self.ctrl[1] = min(aScale*a[1], 1)
            } else {
                self.ctrl[1] = max(aScale*a[1], -1)
            }
        } else if self.ctrlFunc == 2 {
            // Virtual stick control
            self.ctrl = [moveStick[0], moveStick[1], tiltStick[1], -tiltStick[0]]
        }
    }
    
    func control_logic(k: Int) -> (Double, Double, Double, Double){
        // Unpack states
        let xp = self.xp
        let yp = self.yp
        // let lp = self.lp
        let tp = self.tp
        let dxp = self.dxp
        // let dyp = self.dyp
        // let dlp = self.dlp
        // let dtp = self.dtp
        
        // Initialize outputs
        var Bx = 0.0, By = 0.0, Bl = 0.0, Bth = 0.0
        
        // Control horizontal acceleration based on zero effort miss (ZEM)
        // Subtract 1 secoond to get there early, and subtract 0.1 m to keep the
        // ball moving forward
        let pA = stats.stoolCount % 2
        let tUB = abs(self.timeUntilBounce - 1.0)
        let xD = (self.xI + 10.0 * (Double(p.nPlayer) - 1.0 - Double(pA)) - 0.1)
        let ZEM = xD - xp[k] - dxp[k] * tUB
        if p.userControlled[k][0] {
            if self.ctrl[0] == 0 {
                if dxp[k] == 0 {
                    Bx = 0.0
                } else {
                    Bx = -erf(dxp[k]) // Friction
                }
            } else {
                Bx = self.ctrl[0]
            }
        } else {
            Bx = p.Gx * ZEM
            if Bx > 1.0 {
                Bx = 1.0
            } else if (Bx < -1) || (self.timeUntilBounce < 0 && self.timeUntilBounce > 0) {
                Bx = -1.0
            }
        }
        
        // Control leg extension based on timing, turn on when impact in <0.2 sec
        if p.userControlled[k][1] {
            By = self.ctrl[1]
        } else {
            if (self.timeUntilBounce < 0.6) && (self.timeUntilBounce > 0.4) {
                By = -1.0
            } else if abs(self.timeUntilBounce) < 0.2 {
                By = 1.0
            } else {
                By = 0.0
            }
        }
        
        // Control arm extension based on timing, turn on when impact in <0.2 sec
        if p.userControlled[k][2] {
            Bl = gs.ctrl[2]
        } else if abs(self.timeUntilBounce) < 0.2 {
            Bl = 1.0
        } else {
            Bl = 0.0
        }
    
        // Control stool angle by pointing at the ball
        let xdiff = xb-xp[k]  // Ball distance - player distance
        let ydiff = yb-yp[k] - p.d
        let wantAngle = atan2(-xdiff, ydiff)
        if p.userControlled[k][3] {
            Bth = self.ctrl[3]
        } else {
            Bth = p.Gt*(wantAngle-tp[k])
        }
        if Bth > 1.0 {
            Bth = 1.0
        } else if Bth < -1 || (self.timeUntilBounce > 0.0 && self.timeUntilBounce < 0.17) {
            Bth = -1.0
        }
        
        return (Bx*p.Qx, By*p.Qy, Bl*p.Ql, Bth*p.Qt)
    }
    
    func playerAndStool(u: [Double]) -> [Double] {
        // Unpack states
        let yp = self.yp
        let lp = self.lp
        let tp = self.tp
        let dxp = self.dxp
        let dyp = self.dyp
        let dlp = self.dlp
        let dtp = self.dtp
        
        // Initialize output
        var du = Array(repeating: 0.0, count: 20)
        du[0...3] = [self.dxb, self.dyb, 0, -p.g]  // Ball velocities and accelerations
        
        // Loop over players
        var s = 0.0, c = 0.0, Qx = 0.0, Qy = 0.0, Ql = 0.0, Qth = 0.0, ddq = [Double](), i1 = 0, i2 = 0
        for k in 0 ..< p.nPlayer {
            // Sines and cosines of the stool angle
            s = sin(tp[k])
            c = cos(tp[k])
            
            // Control inputs form the generalized forces
            (Qx, Qy, Ql, Qth) = self.control_logic(k: k)

            // Equations of motion, created in the Jupyter notebook eom.ipynb
            ddq = Array(repeating: 0.0, count: 4)
            ddq[0] = 1.0*(-p.Cl*dlp[k]*lp[k]*s - p.Ct*dtp[k]*c - p.Cx*dxp[k]*lp[k] + p.Kl*p.l0*lp[k]*s - p.Kl*pow(lp[k],2)*s - p.Kt*tp[k]*c + Ql*lp[k]*s + Qth*c + Qx*lp[k])/(p.mc*lp[k])
            ddq[1] = (-1.0*(p.Ct*dtp[k] + 1.0*p.Kt*tp[k] - Qth + 2.0*dlp[k]*dtp[k]*p.mg*lp[k] - p.g*p.mg*lp[k]*s)*s + 1.0*(p.Cl*dlp[k] - p.Kl*p.l0 + p.Kl*lp[k] - Ql - pow(dtp[k],2)*p.mg*lp[k] + p.g*p.mg*c)*lp[k]*c - 1.0*(1.0*p.Cy*dyp[k] - 1.0*p.Ky*p.y0 + 1.0*p.Ky*yp[k] - 1.0*Qy - 2.0*dlp[k]*dtp[k]*p.mg*s - 1.0*pow(dtp[k],2)*p.mg*lp[k]*c + 1.0*p.g*p.mc + 1.0*p.g*p.mg)*lp[k])/(p.mc*lp[k])
            ddq[2] = -1.0*p.Cl*dlp[k]/p.mg - 1.0*p.Cl*dlp[k]/p.mc - 1.0*p.Cx*dxp[k]*s/p.mc + 1.0*p.Cy*dyp[k]*c/p.mc + 1.0*p.Kl*p.l0/p.mg + 1.0*p.Kl*p.l0/p.mc - 1.0*p.Kl*lp[k]/p.mg - 1.0*p.Kl*lp[k]/p.mc - 1.0*p.Ky*p.y0*c/p.mc + 1.0*p.Ky*yp[k]*c/p.mc + 1.0*Ql/p.mg + 1.0*Ql/p.mc + 1.0*Qx*s/p.mc - 1.0*Qy*c/p.mc + 1.0*pow(dtp[k],2)*lp[k]
            ddq[3] = (-1.0*p.Ct*dtp[k]*p.mc - 1.0*p.Ct*dtp[k]*p.mg - 1.0*p.Cx*dxp[k]*p.mg*lp[k]*c - 1.0*p.Cy*dyp[k]*p.mg*lp[k]*s - 1.0*p.Kt*p.mc*tp[k] - 1.0*p.Kt*p.mg*tp[k] + 1.0*p.Ky*p.mg*p.y0*lp[k]*s - 1.0*p.Ky*p.mg*lp[k]*yp[k]*s + 1.0*Qth*p.mc + 1.0*Qth*p.mg + 1.0*Qx*p.mg*lp[k]*c + 1.0*Qy*p.mg*lp[k]*s - 2.0*dlp[k]*dtp[k]*p.mc*p.mg*lp[k])/(p.mc*p.mg*pow(lp[k],2))

            // Output State Derivatives
            i1 = k * 8 + 4
            i2 = k * 8 + 12
            du[i1...i2] = [dxp[k], dyp[k], dlp[k], dtp[k], ddq[0], ddq[1], ddq[2], ddq[3]]
            
        }
        
        return du
    }
    
    // Execute a simulation step of duration dt
    func sim_step() {
        // Increment n
        self.n += 1
        
        // Active player
        let pAct = stats.stoolCount % p.nPlayer
        
        // Initial assumption, there was no event
        self.StoolBounce = false
        self.FloorBounce = false
        
        // Prevent event detection if there was already one within 0.1 seconds,
        // or if the ball is far from the stool or ground
        let L = ballHitStool(t: self.t, u: self.u, k: pAct)  // Distance to stool
        let vBall = [self.dxb, self.dyb] // Velocity
        let sBall = norm(vec: vBall)     // Speed
        
        // Set the timing
        var time_condition = -1.0
        if sBall > 0.0 {
            time_condition = (self.yb - self.yp[pAct] - self.lp[pAct] * cos(self.tp[pAct]) - p.d) / sBall
        } 
        let near_condition = abs(self.xb - self.xp[pAct]) < 1.0
        var ddt =  dt, nStep = p.nEulerSteps
        if 0.0 < time_condition && time_condition < 0.5 && near_condition {
            // Slow speed
            ddt = dt / 3.0
            nStep = 3 * p.nEulerSteps
        }
        
        // Integrate using Euler method
        // Initialize state variables
        var U = [[Double]()]
        let rep = Array(repeating: 0.0, count: 20)
        U.append(self.u)
        for _ in 0 ..< nStep {
            U.append(rep)
        }
        
        var dudt = [Double](), Ls = 0.0, Lf = 0.0, tBreak = 0.0
        for k in 0 ... nStep {
            // Increment time
            self.t += ddt / Double(nStep)
            
            // Calculate the derivatives of states w.r.t. time
            dudt = self.playerAndStool(u: U[k])
            
            // Calculate the states at the next step
            for i in 0 ..< 20 {
                U[k+1][i] = U[k][i] + dudt[i] * Double(ddt) / Double(nStep)
            }
            
            // Check for events
            Ls = ballHitStool(t: self.t, u: U[k+1], k: pAct)
            Lf = ballHitFloor(t: self.t, u: U[k+1])
            if (self.t - self.te) > 0.1 {
                if Ls < 0.0 {
                    self.StoolBounce = true
                }
                if Lf < 0.0 {
                    self.FloorBounce = true
                }
                if self.StoolBounce || self.FloorBounce {
                    self.te = self.t
                    self.ue = U[k+1]
                    tBreak = Double(k) * ddt / Double(nStep)
                    break
                }
            }
        }
        
        // If an event occured, increment the counter, otherwise continue
        if self.StoolBounce || self.FloorBounce {
            // Change ball states depending on if it was a stool or floor bounce
            if self.StoolBounce {
                // Obtain the bounce velocity
                // TBR vBounce, vRecoil = BallBounce(self, stats.stoolCount % p.nPlayer)
                let vBounce = [0.0, 0.0], vRecoil = [0.0, 0.0, 0.0, 0.0]
                self.ue[2] = vBounce[0]
                self.ue[3] = vBounce[1]
        
                // Add  the recoil to the player
                self.ue[8+pAct*8] = self.ue[8+pAct*8] + vRecoil[0]
                self.ue[9+pAct*8] = self.ue[9] + vRecoil[1]
                self.ue[10+pAct*8] = self.ue[10] + vRecoil[2]
                self.ue[11+pAct*8] = self.ue[11] + vRecoil[3]
        
            } else if self.FloorBounce {
                // Reverse direction of the ball
                self.ue[2] = +p.COR * self.ue[2]
                self.ue[3] = -p.COR * self.ue[3]
            }
                
            // Re-initialize from the event states
            self.t += ddt - tBreak
            dudt = self.playerAndStool(u: self.ue)
            for i in 0 ..< 20 {
                self.u = self.ue[i] + dudt[i] * (ddt - tBreak)
            }
        
            // Stuck
            if sqrt(pow(self.u[2], 2) + pow(self.u[3], 2)) < p.dybtol && self.u[1] < 1 {
                self.Stuck = true
            }
        } else {
            // Update states
            self.u = U[nStep]
        }
            
        if self.Stuck {
            self.u[1] = p.rb
            self.u[2] = 0.9999*self.u[2]
            self.u[3] = 0
        }
        
        // Generate the new ball trajectory prediction line
        if self.StoolBounce || self.FloorBounce || self.game_mode < 7 {
            // Predict the future trajectory of the ball
            self.ball_predict()
        }
        
        // Stop the ball from moving if the player hasn't hit space yet
        if self.game_mode < 6 {
            self.t = 0
            self.n = 0
            self.u[0] = p.u0[0]
            self.u[1] = p.u0[1]
        }
        
        // Named states
        self.var_states()
    }
}

var gs = GameState()
print(gs.u)
print(gs.ball_predict())
print(gs.tI)

// Define a class to animate the background screen
class MyBackground {
    // Set size of the background, before updates
    let w_orig = 2400.0
    let h_orig = 400.0
    
    // Number of background images
    let num_bg = 3

    // Initialize dependent variables
    var xpos = 0
    var name = [String]()
    init() {
        // Randomize the start location in the background
        xpos = Int(arc4random_uniform(100)) * num_bg
        
        // Initialize the background images
        // TBR
        for n in 0 ..< num_bg {
            name.append("figs/bg\(n).png")
        }
        print(name)
    }

    // var xmod: Float
    func update(x: Double, m2p: Double, w: Double, h: Double) -> Double {
        // xmod is normalized position of the player between 0 and num_bg
        let xmod = fmod(x+Double(xpos),100.0*Double(num_bg))/100.0
        
        // scf is the scale factor to apply to the background
        let scf = pow(m2p/70.0,0.5)
        
        // Position in the background
        let posInBG = w/2.0-xmod*scf*w_orig
        // TBR
        // let newWidth = w_orig*scf
        // let newHeight = h_orig*scf
        // let lowerBound = Int(h/20.0-5)
        
        if xmod>=0 && xmod<0.5 {
            // scene_drawing.image(self.bg[0],posInBG,lowerBound,newWidth,newHeight)
            // scene_drawing.image(self.bg[1],posInBG-newWidth,lowerBound,newWidth,newHeight)
            print("First Case")
        } else if xmod>=0.5 && xmod<1.5 {
            // scene_drawing.image(self.bg[0],posInBG,lowerBound,newWidth,newHeight)
            // scene_drawing.image(self.bg[1],posInBG+newWidth,lowerBound,newWidth,newHeight)
            print("Second Case")
        } else if xmod>=1.5 && xmod<=2.0 {
            // scene_drawing.image(self.bg[0],posInBG+self.num_bg*newWidth,lowerBound,newWidth,newHeight)
            // scene_drawing.image(self.bg[1],posInBG+newWidth,lowerBound,newWidth,newHeight)
            print("Third Case")
        }
        
        return posInBG
    }
}


var bg = MyBackground()

print("xpos = \(bg.xpos) ")
print("w_orig = \(bg.w_orig) ")
print("h_orig = \(bg.h_orig) ")
print(bg.name)
print(bg.update(x: 320.0, m2p: 40, w: 800, h: 500))
print(xy2p(x: 10,y: 3,m2p: 40, po: 5, w: 800, h: 500))
