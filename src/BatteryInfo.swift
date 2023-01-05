//
//  BarreryInfo.swift
//
//  Copyright (c) 2023 Thomas Harr <xDevThomas@gmail.com>
//
//  MIT Licence. See http://opensource.org/licenses/MIT
//
//  Created on 2023-01-03
//

import IOKit
import Foundation


func convertJSONSerializable(rawValue: Any) -> Any {
    switch rawValue {
    case is NSNumber:
        return rawValue as! NSNumber
    case is NSString:
        return rawValue as! NSString
    case is NSArray:
        let rawArray = rawValue as! NSArray
        let arr = NSMutableArray()
        for rawEntry in rawArray {
            arr.add(convertJSONSerializable(rawValue: rawEntry))
        }
        return arr
    case is NSDictionary:
        let rawDictionary = rawValue as! NSDictionary
        let dict = NSMutableDictionary()
        for (rawDictKey, rawDictValue) in rawDictionary {
            dict[convertJSONSerializable(rawValue: rawDictKey)] = convertJSONSerializable(rawValue: rawDictValue)
        }
        return dict
    case is NSData:
        return (rawValue as! NSData).hexEncodedString()
    default:
        return NSString(format: "Unknown type: '%s'", String(describing: type(of: rawValue)))
    }
}


extension NSData {
    struct HexEncodingOptions: OptionSet {
        let rawValue: Int
        static let upperCase = HexEncodingOptions(rawValue: 1 << 0)
    }

    func hexEncodedString(options: HexEncodingOptions = []) -> String {
        let format = options.contains(.upperCase) ? "%02hhX" : "%02hhx"
        return self.map { String(format: format, $0) }.joined()
    }
}


var serviceIterator: io_iterator_t = io_iterator_t()

var waittime = mach_timespec_t(tv_sec: 1,tv_nsec: 0)
IOServiceWaitQuiet(kIOMainPortDefault, &waittime)

if (IOServiceGetMatchingServices(kIOMainPortDefault, IOServiceNameMatching("AppleSmartBattery"), &serviceIterator) == kIOReturnSuccess) {
    IOIteratorReset(serviceIterator)

    repeat {
        let service: io_service_t = IOIteratorNext(serviceIterator)
        // Check if there is a service
        guard service != 0 else {
            break
        }

        var serviceProperties: Unmanaged<CFMutableDictionary>?
        IORegistryEntryCreateCFProperties(service, &serviceProperties, kCFAllocatorDefault, 0)
        let serviceEntries = NSDictionary(dictionary:(serviceProperties?.takeUnretainedValue())!)

        do {
            let batteryData = try JSONSerialization.data(withJSONObject: convertJSONSerializable(rawValue: serviceEntries))
            print(NSString(data: batteryData, encoding: String.Encoding.utf8.rawValue)! as String)
        } catch {
            print(error)
        }

        serviceProperties?.release()
        IOObjectRelease(service)

    } while(IOIteratorIsValid(serviceIterator) == boolean_t(truncating: true))
}
