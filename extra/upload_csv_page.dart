import 'dart:io';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter/material.dart';
import 'package:csv/csv.dart';

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  Future<void> _uploadCSV() async {
    // Path to the CSV file
    final filePath = 'DummyMyntraDataset2.csv';
    
    // Read the CSV file
    final input = File(filePath).openRead();
    final fields = await input.transform(utf8.decoder).transform(CsvToListConverter()).toList();

    // Assuming first row contains headers
    List<String> headers = fields[0].cast<String>();

    // Prepare data to upload
    List<Map<String, dynamic>> data = [];
    for (var i = 1; i < fields.length; i++) {
      Map<String, dynamic> row = {};
      for (var j = 0; j < headers.length; j++) {
        row[headers[j]] = fields[i][j];
      }
      data.add(row);
    }

    // Upload data to Firestore
    for (var item in data) {
      await FirebaseFirestore.instance.collection('recommendations').add(item);
    }

    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Data uploaded successfully!')));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Upload CSV to Firebase'),
      ),
      body: Center(
        child: ElevatedButton(
          onPressed: _uploadCSV,
          child: Text('Upload CSV'),
        ),
      ),
    );
  }
}
