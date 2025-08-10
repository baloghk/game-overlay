package com.overlay.demo.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api/items")
public class ItemIdentifyController {

    @PostMapping("/identify")
    public ResponseEntity<String> identifyItem(@RequestParam("file") MultipartFile file) {
        

        if (file.isEmpty()) {
            return ResponseEntity.badRequest().body("No file uploaded");
        }

        try {
            String fileName = file.getOriginalFilename();
            long size = file.getSize();

            return ResponseEntity.ok("Received: " + fileName + " (" + size + " bytes) → This is a TEST item");
        } catch (Exception e) {
            return ResponseEntity.internalServerError().body("Error: " + e.getMessage());
        }
    }
}
