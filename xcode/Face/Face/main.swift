//
//  main.swift
//  facial_extractor
//
//  Created by Sal Faris on 17/02/2024.
//

import Vision
import CoreGraphics
import Foundation
import Cocoa


private let VERSION  = 1.8

// MARK: Functions used by the ffrecognition Library to install
@_cdecl("_install_application_support")
public func _install_application_support() -> CString{
    let appSupports = FileManager.default.urls(for: .applicationSupportDirectory, in: .userDomainMask)
    if let appSupport = appSupports.first{
        return CString(appSupport.path(percentEncoded: false))
    }else{
        fatalError("Unable to find Application Support Path.")
    }
}


// MARK: Private Functions
private func fetchIpd(_ id: Int) -> ImageProcessedData{
    if let object = referenceTable[id]{
        return object
    }else{
        fatalError("Unable to lookup ID: \(id)")
    }
}


// MARK: Reference Table for Swift when Python calls
private var referenceTable: [Int: ImageProcessedData] = {
    print("Acclerated by face.dylib version \(VERSION) 🚀")
    return [:]
}()


// MARK: Public Functions for PySIGen to create Python Bindings for
@_cdecl("ipd_init_image")
public func ipd_init_image(_ imagePath: CString) -> Int{
    let id = Int.random(in: 0000000...9999999)
    if let nsImage = NSImage(contentsOf: imagePath.toString().toURLPath()){
        referenceTable[id] = .init(image:  nsImage.cgImage())
    }else{
        fatalError("Unable to create NSImage from path provided: \(imagePath.toString())")
    }
    
    return id
}







// Returns the images of faces as base64 encoded strings in a JSON array
@_cdecl("ipd_faces")
public func ipd_faces(id: Int) -> CString{
    let object = fetchIpd(id)
    object.cropAllFaces()
    let faceImages = object.facesImages.compactMap { image in
        return image.data().base64EncodedString()
    }
    
    let json_swift = FaceImagesRAW64(faces: faceImages)
    return CString(json_swift)
}



@_cdecl("mem_dealloc_ipd")
public func funcmem_dealloc_ipd(_ id: Int){
    referenceTable.removeValue(forKey: id)
}



// MARK: Testing...

//let directory = "/Users/Salman/Pictures/Photos Library.photoslibrary/originals/0"
//let files = try! FileManager.default.contentsOfDirectory(at: .init(filePath: directory), includingPropertiesForKeys: [.isRegularFileKey])
//let paths = files.compactMap { url in
//    return url.path(percentEncoded:false)
//}
//
//let filteredPaths = paths.filter { string in
//    
//    let notSupported = ["aae", "mov", "mp4"]
//    
//    for notSupport in notSupported {
//        if string.hasSuffix(notSupport){
//            return false
//        }
//    }
//    
//    return true
//}


//
//let batch_item = BATCH_ImagePaths(paths: filteredPaths)
//let encoded = CString(String(data: try! JSONEncoder().encode(batch_item), encoding: .utf8)!)
//let ids = try! JSONDecoder().decode(BATCH_ImageIds.self, from: ipd_batch_init_image(encoded).toString().data(using: .utf8)!)
//checkSpeed (label: "Cropped Faces") {
//    _ = ipd_batch_faces(.init(ids))
//}
//
