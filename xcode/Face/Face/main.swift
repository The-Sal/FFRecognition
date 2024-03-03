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


private let VERSION  = 0.1

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
    print("Accelerated by face.dylib version \(VERSION) 🚀")
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


@_cdecl("ipd_batch_init_image")
public func ipd_batch_init_image(_ paths: CString) -> CString{
    let object = try! JSONDecoder().decode(BATCH_ImagePaths.self, from: paths.toString().data(using: .utf8)!)
    var ids: [Int] = []
    for path in object.paths{
        ids.append(ipd_init_image(.init(path)))
    }
    
    let returnObject = BATCH_ImageIds(ids: ids)
    return CString(returnObject)
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

@_cdecl("ipd_batch_faces")
public func ipd_batch_faces(_ ids: CString) -> CString{
    let ids = try! JSONDecoder().decode(BATCH_ImageIds.self, from: ids.toString().data(using: .utf8)!)
    
    var arrayOfFaces: [FaceImagesRAW64] = []
    
    for id in ids.ids{
        arrayOfFaces.append(try! JSONDecoder().decode(FaceImagesRAW64.self, from: ipd_faces(id: id).toString().data(using: .utf8)!))
    }
    
    return CString(BATCH_FaceImagesRAW64(array: arrayOfFaces))
}

@_cdecl("mem_dealloc_ipd")
public func funcmem_dealloc_ipd(_ id: Int){
    _ = referenceTable.removeValue(forKey: id)
}



