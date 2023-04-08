import 'dart:convert';
import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'websocket.dart';

class VideoStream extends StatefulWidget {
  const VideoStream({Key? key}) : super(key: key);

  @override
  State<VideoStream> createState() => _VideoStreamState();
}

class _VideoStreamState extends State<VideoStream> {
  final WebSocket _socket = WebSocket("ws://localhost:5000");
  bool _isConnected = false;
  void connect(BuildContext context) async {
    _socket.connect();
    setState(() {
      _isConnected = true;
    });
  }

  void disconnect() {
    _socket.disconnect();
    setState(() {
      _isConnected = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Live Video"),
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                ElevatedButton(
                  onPressed: () => connect(context),
                  child: const Text("Connect"),
                ),
                ElevatedButton(
                  onPressed: disconnect,
                  child: const Text("Disconnect"),
                ),
              ],
            ),
            const SizedBox(
              height: 50.0,
            ),
            _isConnected
                ? StreamBuilder(
                    stream: _socket.stream,
                    builder: (context, snapshot) {
                      if (!snapshot.hasData) {
                        return const CircularProgressIndicator();
                      }

                      if (snapshot.connectionState == ConnectionState.done) {
                        return const Center(
                          child: Text("Connection Closed !"),
                        );
                      }
                      //? Working for single frames
                      Map<String, dynamic> response = json.decode(snapshot.data);
                      return Image.memory(
                        Uint8List.fromList(
                          base64Decode(
                            (response["second_section"].toString()),
                          ),
                        ),
                        gaplessPlayback: true,
                        excludeFromSemantics: true,
                      );
                    },
                  )
                : const Text("Initiate Connection")
          ],
        ),
      ),
    );
  }
}
