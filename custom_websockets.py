import json

def handle_websockets(data):
    parsed_fields = parse_ws_frame(data)
    if parsed_fields != None:
        if parsed_fields == False: # If the opcode was detected as closing connection
            self.open_ws_connections.remove(self.request) # Remove from list of open connections
            print("removed an open ws connection, now total is: "+str(len(self.open_ws_connections)), flush=True)
            return # Return to exit handle()
        else: # Else, the frame did contain a body and buffer_ws_frame() returned it in bytes
            
            # Obtain messageType
            body_dict: dict = json.loads(parsed_fields["masked_and_sanitized_body"])
            message_type = body_dict["messageType"]
            print(f"=> message_type was: {message_type}", flush=True)

            print("=> the bytes of size ["+str(len(data))+"] were: "+str(data), flush=True)
            for key in parsed_fields:
                if (key != "body") and (key != "masked_and_sanatized_body"):
                    print("--> "+key+" was: "+str(parsed_fields[key]), flush=True)

            if message_type == "chatMessage":
                response_body = add_generated_username(parsed_fields["masked_and_sanitized_body"], username)
                store_chat_data(response_body)
                response_frame = generate_ws_response_frame(self, parsed_fields["opcode"], response_body)
                print("=> response_frame was: "+str(response_frame), flush=True)

                for connection in self.open_ws_connections: # Send to all open connections, only
                    connection.sendall(response_frame)
            elif (message_type == "webRTC-offer") or (message_type == "webRTC-answer") or\
                (message_type == "webRTC-candidate"):

                response_body: bytes = parsed_fields["masked_and_sanitized_body"] # TODO try not santaizing
                response_frame = generate_ws_response_frame(self, parsed_fields["opcode"], response_body)
                # print("=> response_frame was: "+str(response_frame), flush=True)

                for connection in self.open_ws_connections: # Send to all open connections that aren't this connection
                    if connection != self.request:
                        connection.sendall(response_frame)

send_text = int('00000001', 2)
close_connection = int('00001000', 2)

def parse_ws_frame(data: bytes):
    """
    Bit parses a WebSocket frame and returns a dict opcode and final payload length NOT including the body data
    """
    fields = {} # Collection DS of: WS frame fields -> their values

    # NOTE: Python bitwise operations work in int's
    [spliced_data, data] = splice_and_update_data(data, 1) # Found out putting multiple return vals into list isn't necessary, but good visually    
    opcode = bitwise_and(spliced_data, '00001111') # First byte and Mask: Half Byte right
    fields["opcode"] = opcode
    
    if opcode == send_text: # Go forward with parsing the content
        [spliced_data, data] = splice_and_update_data(data, 1)
        payload_len: int = bitwise_and(spliced_data, '01111111') # Second byte and Mask: 7 rightmost bits (we assume MASK bit = 1)
        fields["payload_len"] = payload_len # FOR DEBUGGING

        final_payload_length: int = 0 # int with unit: bytes. Set initially to 0, to be updated in the if-else blocks
        if payload_len == med_payload_len:
            # Read the next 2 bytes
            [spliced_data, data] = splice_and_update_data(data, 2)
            final_payload_length = to_int(spliced_data)
        elif payload_len == large_payload_len:
            # Read the next 8 bytes
            [spliced_data, data] = splice_and_update_data(data, 8)
            final_payload_length = to_int(spliced_data)
        else: # else the payload_len value itself is the payload length
            final_payload_length = payload_len # This could be implicit by setting fpl default to payload_len but this is for clarity

        fields["final_payload_length"] = final_payload_length

        [spliced_data, data] = splice_and_update_data(data, 4) # Obtain 4-byte masking key
        masking_key = spliced_data
        fields["masking_key"] = masking_key

        body = data # All the remaining bytes after the masking key will the body
        fields["body"] = body # This is for when you get to buffering

        # NOTE: REMOVE this if you are buffering. This is only used when not buffering, and will break things if buffering occurs.
        # masked_body = mask_ws_data(body, fields["masking_key"], final_payload_length)
        # masked_body = masked_body.replace(b'&', b'&amp;').replace(b'<', b'&lt;').replace(b'>', b'&gt;') # Sanitize HTML
        # fields["masked_and_sanitized_body"] = masked_body

    return fields