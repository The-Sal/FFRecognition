//
//  classes.swift
//  facial_extractor
//
//  Created by Sal Faris on 21/02/2024.
//

import Foundation
import Vision
import Cocoa

public typealias CString = UnsafePointer<Int8>



extension CString{
    init(_ json: Codable){
        self.init(strdup(String(data: try! JSONEncoder().encode(json), encoding: .utf8)!))!
    }
    init(_ string: String){
        self.init(strdup(string))!
    }
    
    func toString() -> String{
        return String(cString: self)
    }
}



extension String{
    func toCString() -> CString{
        return CString(self)
    }
    
    func toURLPath() -> URL{
        return URL(filePath: self)
    }
    
}


extension NSImage{
    func cgImage() -> CGImage{
        if let cgImage = self.cgImage(forProposedRect: nil, context: nil, hints: nil){
            return cgImage
        }else{
            fatalError("Unable to convert NSImage to CGImage")
        }
        
    }
}

extension CGImage {
    func data() -> Data{
        let nsImage = NSImage(cgImage: self, size: .zero)
        if let tiffData = nsImage.tiffRepresentation,
           let bitmap = NSBitmapImageRep(data: tiffData) {
            let pngData = bitmap.representation(using: .png, properties: [:])
            return pngData!
        }
        
        fatalError("Unable to convert NSImage to Binary Data")
    }
}


// A JSON struct to be able to Pass Images as Binary data in an array
struct FaceImagesRAW64: Codable{
    var faces: [String]
}

struct BATCH_ImagePaths: Codable{
    var paths: [String]
}

struct BATCH_ImageIds: Codable{
    var ids: [Int]
}

struct BATCH_FaceImagesRAW64: Codable{
    var array: [FaceImagesRAW64]
}


public class ImageProcessedData{
    var image: CGImage
    var faces: [VNFaceObservation]
    var facesImages: [CGImage] = []
    var boundingBoxesForFace: [CGImage: CGRect] = [:]
    
    
    init(image: CGImage) {
        self.image = image
        
        
        var output: [VNFaceObservation] = []
        let imageRequestHandler = VNImageRequestHandler(cgImage: image)
        let rectangleRequest = VNDetectFaceRectanglesRequest { request, error in
            
            if let result = request.results{
                let observations = result as! [VNFaceObservation] // one observation per face found in an image
                output = observations
            }
            
        }
        
        rectangleRequest.preferBackgroundProcessing = false
        rectangleRequest.revision = VNDetectFaceRectanglesRequestRevision3
        try! imageRequestHandler.perform([rectangleRequest])
        
        self.faces = output
        
    }
    
    
    // use the VNFaceObservartion to cropt he 'image' into all the different faces
    func cropAllFaces(){
        self.facesImages.removeAll()
        for face in faces {
            let bounding = face.boundingBox
            
            // dimensions of the CGRect
            let w = bounding.width * CGFloat(self.image.width)
            let h = bounding.height * CGFloat(self.image.height)
            let x = bounding.origin.x * CGFloat(self.image.width)
            let y = (1 - bounding.origin.y) * CGFloat(self.image.height) - h
            
            let rect = CGRect(x: x, y: y, width: w, height: h)
            let cropped = self.image.cropping(to: rect)!
            self.facesImages.append(cropped)
        }
        
    }
    
    
}
