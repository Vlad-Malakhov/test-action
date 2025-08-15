# if a and b and c and a or not c and a:
#   a = b + 1
# print (a)
# if a == b and a == b and a == b:
#   print(a)
#   b = a
# print(b)
# if b == c:
#   print(b)
# if a == b and a == b and a == b:
#   print(b)
# for _ in range(10):
#         if np.all(b.c.d[:, :, :, : -1] > 240):
#             f.g(20, True)
#         if np.all(b.c.d[:, :, :, :, : -1] > 240):
#             f.g(20, True)
#         if np.all(zebra.white_tensor.black_tensor[:, -1] >= 240) or np.all(b.c.d[:, :, :, : -1] > 240):
#             f.g(20, True)
#         else:
#             break

  # Handle FFN and prefill conversions (both chunked and non-chunked)
    if split_part in ['2', '2_prefill']:
        converted_models = []
        chunks_to_process = range(num_chunks)
        
        for i in chunks_to_process:
            # Use FFN in filename for mode '2', keep simple prefill for '2_prefill'
            base_name = f'{prefix}_FFN' if split_part == '2' else f'{prefix}_prefill'
            if lut_bits is not None:
                base_name += f'_lut{lut_bits}'
            chunk_output_path = f"{base_name}_chunk_{i+1:02d}of{num_chunks:02d}.mlpackage"
            
            print(f"\nConverting chunk {i+1}/{num_chunks}")
            
            # Clean up before converting next chunk
            import gc
            gc.collect()
            
            # For single chunk (num_chunks=1), don't pass chunk_idx
            chunk_idx = i if num_chunks > 1 else None
            
            if split_part == '2':
                chunk_model = converter.convert_FFN(model, chunk_idx=i)
            else:  # '2_prefill'
                chunk_model = converter.convert_prefill(model, chunk_idx=i)
                
            if chunk_output_path:
                # Add metadata before saving
                AddMetadata(chunk_model, {
                    'context_length': context_length,
                    'num_chunks': num_chunks,
                    'chunk_no': i+1,
                    'batch_size': batch_size if split_part in ['2_prefill'] else None,
                    'lut_bits': lut_bits,
                    'split_part': split_part
                })
                print(f"Saving chunk to {chunk_output_path}")
                chunk_output_path = os.path.join(output_dir, chunk_output_path)
                chunk_model.save(chunk_output_path)
                
            converted_models.append(chunk_model)
            
            # Clean up after saving
            del chunk_model
            gc.collect()
            
            # Small delay to ensure cleanup
            import time
            time.sleep(1)
            
        return converted_models
    else:
        # Convert model based on split_part
        
        if split_part == '1':
            base_name = f'{prefix}_embeddings'
        elif split_part == '3':
            base_name = f'{prefix}_lm_head'
        elif split_part == '123':
            base_name = f'{prefix}_'
        else:
            raise ValueError(f"Invalid split_part: {split_part}")
        if lut_bits is not None:
            base_name += f'_lut{lut_bits}'
        output_path = f"{base_name}.mlpackage"
        print(f"\nConverting model part: {split_part} output_path: {output_path}")
        converted_model = converter.convert(split_part=split_part)
        #print(f"converted_model: {converted_model}")
        
        # Add metadata before saving
        if output_path:
            if isinstance(converted_model, list):
                # Handle multi-part models (123 mode)
                for i, chunk_model in enumerate(converted_model):
                    AddMetadata(chunk_model, {
                        'context_length': context_length,
                        'num_chunks': num_chunks,
                        'chunk_no': i+1,
                        'batch_size': batch_size if split_part in ['2_prefill'] else None,
                        'lut_bits': lut_bits,
                        'split_part': split_part
                    })
                    chunk_output_path = output_path.replace('.mlpackage', f'_{i+1}.mlpackage')
                    print(f"Saving chunk to {chunk_output_path}")
                    chunk_output_path = os.path.join(output_dir, chunk_output_path)
                    chunk_model.save(chunk_output_path)
            else:
                # Handle single model parts
                AddMetadata(converted_model, {
                    'context_length': context_length,
                    'batch_size': batch_size if split_part in ['2_prefill'] else None,
                    'lut_bits': lut_bits,
                    'split_part': split_part
                })
                print(f"Saving model to {output_path}")
                output_path = os.path.join(output_dir, output_path)
                converted_model.save(output_path)
        
        print("\nModel verification:")
        if isinstance(converted_model, list):
            # For multi-part models, use chunk numbers instead of hardcoded component names
            for i, model in enumerate(converted_model):
                print(f"\nChunk {i+1}:")
                print(f"Input names: {model.input_description}")
                print(f"Output names: {model.output_description}")
        else:
            print(f"Input names: {converted_model.input_description}")
            print(f"Output names: {converted_model.output_description}")
        
        return converted_model

