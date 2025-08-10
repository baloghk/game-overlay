package com.overlay.demo.controller;

import com.overlay.demo.models.Item;
import com.overlay.demo.repository.ItemRepository;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api/items")
public class ItemController {

    private final ItemRepository ir;

    public ItemController(ItemRepository ir) {
        this.ir = ir;
    }

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

    @PostMapping
    public Item addItem(@RequestBody Item item) {
        return ir.save(item);
    }

    @GetMapping
    public java.util.List<Item> getAllItems() {
        return ir.findAll();
    }
}
