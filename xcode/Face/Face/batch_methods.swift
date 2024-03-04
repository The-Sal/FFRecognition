//
//  batch_methods.swift
//  Face
//
//  Created by Sal Faris on 04/03/2024.
//

import Cocoa
import Foundation
import AppKit



/*
 Can't be split into different threads. Vision Framework causes a deadlock for some reason. Faster Running it in series
 */
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


@_cdecl("ipd_batch_faces")
public func ipd_batch_faces(_ ids: CString) -> CString {
    let idsObject = try! JSONDecoder().decode(BATCH_ImageIds.self, from: ids.toString().data(using: .utf8)!)
    
    
    var arrayOfFaces: [FaceImagesRAW64] = []
    let group = DispatchGroup()
    let queue = DispatchQueue.global(qos: .userInitiated)
    
    
    for id in idsObject.ids{
        group.enter()
        queue.async {
            let faceRAW = try! JSONDecoder().decode(FaceImagesRAW64.self, from: ipd_faces(id: id).toString().data(using: .utf8)!)
            arrayOfFaces.append(faceRAW)
            group.leave()
        }
        
    }
    
    
    group.wait() // Wait for all tasks to complete
    
    let returnObject = BATCH_FaceImagesRAW64(array: arrayOfFaces)
    return CString(returnObject)
}
