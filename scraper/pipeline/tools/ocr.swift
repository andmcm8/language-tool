// macOS Vision OCR: swift ocr.swift <image-or-pdf> ... -> prints recognized text (reading order)
import Foundation
import Vision
import AppKit
import PDFKit

func ocr(_ cg: CGImage) -> String {
    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    req.usesLanguageCorrection = false
    let h = VNImageRequestHandler(cgImage: cg, options: [:])
    try? h.perform([req])
    let obs = (req.results ?? []).sorted { a, b in
        let dy = a.boundingBox.midY - b.boundingBox.midY
        if abs(dy) > 0.01 { return dy > 0 }
        return a.boundingBox.minX < b.boundingBox.minX
    }
    return obs.compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\n")
}

for path in CommandLine.arguments.dropFirst() {
    let url = URL(fileURLWithPath: path)
    if path.lowercased().hasSuffix(".pdf"), let doc = PDFDocument(url: url) {
        for i in 0..<min(doc.pageCount, 12) {
            guard let page = doc.page(at: i) else { continue }
            let r = page.bounds(for: .mediaBox)
            let scale: CGFloat = 2.5
            let img = NSImage(size: NSSize(width: r.width * scale, height: r.height * scale))
            img.lockFocus()
            NSColor.white.set(); NSRect(origin: .zero, size: img.size).fill()
            let ctx = NSGraphicsContext.current!.cgContext
            ctx.scaleBy(x: scale, y: scale)
            page.draw(with: .mediaBox, to: ctx)
            img.unlockFocus()
            if let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) { print(ocr(cg)) }
        }
    } else if let img = NSImage(contentsOf: url), let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) {
        print(ocr(cg))
    }
}
