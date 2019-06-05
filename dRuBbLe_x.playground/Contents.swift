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

let pi = 3.14159

// Convert physical coordinates to pixels
func xy2p(x: Double,y: Double, m2p: Double,po: Double,w: Double,h: Double) -> (Double, Double) {
    let xout = x*m2p-po+w/2
    let yout = y*m2p+h/20
    return (xout, yout)
}

// Set up the parameter class
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

// Animate the background screen
class MyBackground {
    // Set size of the background, before updates
    let w_orig = 2400.0
    let h_orig = 400.0
    
    // Number of background images
    let num_bg = Int(3)

    // Initialize dependent variables
    var xpos: Int
    var name = [String]()
    init() {
        // Randomize the start location in the background
        xpos = arc4random_uniform(100) * num_bg
        
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
