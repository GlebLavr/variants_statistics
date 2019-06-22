task variants_count{
    File input_file
    String output_file
    command {
        python /home/usr/variants.py ${input_file} ${output_file}
    }
    output{
        File dest = "${output_file}"
    }
    runtime {
        docker: 'gleblavr/variants'
    }
}

workflow variants_wf {
    call variants_count
}
