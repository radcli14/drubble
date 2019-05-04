import UIKit

// Timing variables
let fs = 60.0
let dt = 1/fs

// For keyboard input, set the state of the arrows and W-A-S-D
var keyPush = [0,0,0,0,0,0,0,0]

// Color definition
let red       = (1.0,0.0,0.0)
let green     = (0.0,1.0,0.0)
let blue      = (0.0,0.0,1.0)
let darkBlue  = (0.0,0.0,128.0/255.0)
let white     = (1.0,1.0,1.0)
let gray      = (160.0/255.0,160.0/255.0,160.0/255.0)
let black     = (0.0,0.0,0.0)
let pink      = (1.0,100.0/255.0,100.0/255.0)
let skyBlue   = (135.0/255.0, 206.0/255.0, 235.0/255.0)
let darkGreen = (0.0,120.0/255.0,0)

// Convert physical coordinates to pixels
func xy2p(x: Double,y: Double, m2p: Double,po: Double,w: Double,h: Double) -> (Double, Double) {
    let xout = x*m2p-po+w/2
    let yout = y*m2p+h/20
    return (xout, yout)
}

// Animate the background screen
class MyBackground {
    // Set size of the background, before updates
    let w_orig = 2400.0
    let h_orig = 400.0
    
    // Number of background images
    let num_bg = UInt32(3)

    // Initialize dependent variables
    var xpos: UInt32
    var name = [String]()
    init() {
        // Randomize the start location in the background
        xpos = arc4random_uniform(100)*num_bg
        
        // Initialize the background images
        // TBR
        for n in 0 ... num_bg-1 {
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

struct Parameters {
    
}

var bg = MyBackground()

print("xpos = \(bg.xpos) ")
print("w_orig = \(bg.w_orig) ")
print("h_orig = \(bg.h_orig) ")
print(bg.name)
print(bg.update(x: 320.0, m2p: 40, w: 800, h: 500))
print(xy2p(x: 10,y: 3,m2p: 40, po: 5, w: 800, h: 500))