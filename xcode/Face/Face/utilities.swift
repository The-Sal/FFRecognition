//
//  utilities.swift
//  Face
//
//  Created by Sal Faris on 04/03/2024.
//

import Foundation


func checkSpeed(label: String? = nil, block: () -> ()){
    let t = Date.now
    block()
    let now = t.timeIntervalSinceNow
    print("[<\(label ?? "unknown")>] completed in: \(abs(now))")
}
