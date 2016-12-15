from pitrain.section import Section


section_id = 1
section_pin_forward = 17
section_pin_backward = 18
section_length = "120"
section_name = "first_section"

mysection = Section(section_id,
                    section_pin_forward,
                    section_pin_backward,
                    section_length,
                    [],
                    section_name)

for x in range(3):
    mysection.forward(0.6)
    time.sleep(3)
    mysection.stop()
    time.sleep(1)
    mysection.backward(0.6)
    time.sleep(3)
    mysection.stop()
    time.sleep(1)

mysection.stop()

